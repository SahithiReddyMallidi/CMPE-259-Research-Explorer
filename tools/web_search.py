from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

def web_search(query):
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print("Warning: TAVILY_API_KEY not set. Web search disabled.")
        return []

    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query)
        return response.get("results", [])
    except Exception as e:
        print(f"Web search failed: {e}")
        return []