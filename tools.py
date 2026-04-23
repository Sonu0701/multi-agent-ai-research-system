from langchain.tools import tool
from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Tavily client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# ==============================
# 🔍 WEB SEARCH TOOL
# ==============================
@tool
def web_search(query: str) -> str:
    """
    Search the web and return structured results with title, URL, and summary.
    """

    try:
        results = tavily.search(query=query, max_results=5)

        formatted_results = []

        for i, r in enumerate(results["results"], 1):
            formatted_results.append(
                f"[{i}]\n"
                f"Title: {r.get('title', 'N/A')}\n"
                f"URL: {r.get('url', 'N/A')}\n"
                f"Summary: {r.get('content', '')[:200]}"
            )

        return "\n\n".join(formatted_results)

    except Exception as e:
        return f"Search error: {str(e)}"


# ==============================
# 🔗 URL EXTRACTION TOOL
# ==============================
@tool
def extract_urls(text: str) -> str:
    """
    Extract all unique URLs from the given text.
    """

    try:
        urls = re.findall(r'https?://\S+', text)

        unique_urls = list(set(urls))

        if not unique_urls:
            return "No URLs found."

        return "\n".join(unique_urls)

    except Exception as e:
        return f"URL extraction error: {str(e)}"


# ==============================
# 📄 SCRAPER TOOL
# ==============================
@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean readable content from a URL.
    """

    try:
        if not url.startswith("http"):
            return "Invalid URL"

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        if response.status_code != 200:
            return f"Failed to fetch page. Status code: {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        if len(text) < 200:
            return "Content too short or not useful."

        return text[:4000]

    except Exception as e:
        return f"Scraping error: {str(e)}"