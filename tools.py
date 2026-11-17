from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information.
    Returns titles, URLs and snippets of relevant websites."""
    try:
        results = tavily.search(query=query, max_results=3)
        out = []
        for result in results.get("results", []):
            out.append(
                f"""
                Title: {result.get('title', '')}
                URL: {result.get('url', '')}
                Content: {result.get('content', '')[:700]}
                """
            )
        if not out:
            return "No relevant search results found."
        return "\n--------\n".join(out)
    except Exception as e:
        return f"Web search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape a webpage URL and return its clean text content.
    Use this tool to read a webpage in detail."""
    try:
        response = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        content = text[:4000]
        return content if text else "No readable content found."
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

     