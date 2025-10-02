from langchain.tools import BaseTool
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from typing import Type
from pydantic import BaseModel, Field

class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the web")
    
class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web using DuckDuckGo. Only use this if local_search doesn't find relevant information."
    args_schema: Type[BaseModel] = WebSearchInput #type: ignore
    
    def _run(self, query: str) -> str:
        
        try:
            search = DuckDuckGoSearchAPIWrapper()
            results = search.run(query)
            return f"Web search results:\n{results}"
        
        except Exception as e:
            return f"Error searching the web: {str(e)}"
    