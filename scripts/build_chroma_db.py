import json
from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document
from typing import List

def load_news_corpus(corpus_path) -> List[Document]:
    documents = []
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            article = json.loads(line)
            
            doc = Document(
                page_content=f"{article['metadata']['title']}\n\n{article['text']}",
                metadata={
                    "id": article['id'],
                    "title": article['metadata']['title'],
                    "source": article['metadata']['source'],
                    "source_id": article['metadata']['source_id'],
                    "author": article['metadata']['author'],
                    "published_at": article['metadata']['published_at'],
                    "url": article['metadata']['url'],
                    "category": article['metadata']['category'],
                    "trustworthy": article['metadata']['trustworthy'],
                    "language": article['metadata']['language']
                }
            )
            documents.append(doc)
    return documents


def build_chroma_collection(documents, persist_directory= "./chroma_db"):
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large",
    )
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="news_corpus"
    )
    
    return vectorstore        

def main():
    corpus_dir = Path("./data/corpus")
    corpus_files = list(corpus_dir.glob("news_corpus_*.jsonl"))
    
    if not corpus_files:
        print("❌ No corpus files found!")
        print("Please run build_corpus.py first to fetch news articles.")
        return
    
    latest_corpus = max(corpus_files, key=lambda p: p.stat().st_mtime)
    print(f"📰 Loading corpus: {latest_corpus.name}")
    
    # Load documents
    documents = load_news_corpus(latest_corpus)
    print(f"📄 Loaded {len(documents)} articles")
    
    # Build ChromaDB
    vectorstore = build_chroma_collection(documents)
    
if __name__ == "__main__":
       main()   
    