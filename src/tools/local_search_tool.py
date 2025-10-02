from langchain.tools import BaseTool
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from typing import Optional,Type
from pydantic import BaseModel, Field


class LocalSearchInput(BaseModel):
    query: str = Field(description="The search query to look up in the local database")


class LocalSearchTool(BaseTool):
    name: str = "local_search"
    description: str = "Search the local ChromaDB database for relevant news articles and information. Use this first before trying web search."
    args_schema: Type[BaseModel] = LocalSearchInput #type: ignore
    vectorstore: Optional[Chroma] = None
    
    def __init__(self):
        super().__init__()
        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings,
            collection_name="news_corpus"
        )
    
    def _run(self, query: str) -> str:
        try:
            if self.vectorstore is None:
                return "Vector store not initialized."
            
            results = self.vectorstore.similarity_search_with_score(query, k=3)
            
            if not results:
                return "No relevant information found in local database."
            
            response = "Found in local database:\n\n"
            for i, (doc, score) in enumerate(results, 1):
                response += f"Result {i} (relevance: {1-score:.2f}):\n"
                response += f"Title: {doc.metadata.get('title', 'N/A')}\n"
                response += f"Source: {doc.metadata.get('source', 'N/A')}\n"
                response += f"Author: {doc.metadata.get('author', 'N/A')}\n"
                response += f"Published: {doc.metadata.get('published_at', 'N/A')}\n"
                response += f"Category: {doc.metadata.get('category', 'N/A')}\n"
                response += f"Trustworthy: {doc.metadata.get('trustworthy', 'N/A')}\n"
                response += f"URL: {doc.metadata.get('url', 'N/A')}\n"
                response += f"\nFull Text:\n{doc.page_content}\n"
            
            return response
        
        except Exception as e:
            return f"Error searching local database: {str(e)}"
