from langchain.tools import BaseTool
from typing import Type 
from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun

class SearchInput(BaseModel):
    query: str = Field(description="The search query to look up")

class SearchTool(BaseTool):
    name: str = "search"
    description: str = "Useful for searching information on the internet"
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        try:
           # This is a simple implementation using DuckDuckGo
           tool = DuckDuckGoSearchRun()
           return tool.invoke(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"

    async def _arun(self, query: str) -> str:
        return self._run(query) 