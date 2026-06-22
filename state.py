from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    topic: str
    search_results: str
    scraped_content: str
    report: str
    feedback: str
    score: int
    retry_count: int
    urls: str
    