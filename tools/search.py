from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from tavily import TavilyClient

tavily_client = TavilyClient()


@tool
def search_web(query:str) -> str:
    """Search web for information"""
    return tavily_client.search(query)
