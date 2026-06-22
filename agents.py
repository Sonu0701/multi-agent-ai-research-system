from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.prebuilt import create_react_agent
from tools import web_search, scrape_url, extract_urls
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("MISTRAL_API_KEY"):
    raise ValueError("MISTRAL_API_KEY missing")

llm = ChatMistralAI(model="mistral-small", temperature=0.2)

# Search Agent (uses web_search tool)
search_agent = create_react_agent(
    model=llm,
    tools=[web_search],
    prompt="""You are a research search specialist.
Search for accurate, recent, relevant information using web_search.
Return structured results with titles, URLs, and summaries.
Always prefer trusted sources. Do NOT hallucinate."""
)

# URL Extractor Agent
url_agent = create_react_agent(
    model=llm,
    tools=[extract_urls],
    prompt="""You are a URL extraction assistant.
Extract all valid URLs from the given text using extract_urls tool.
Remove duplicates. Return only clean URLs. No extra explanation."""
)

# Reader Agent (uses scrape_url tool)
reader_agent = create_react_agent(
    model=llm,
    tools=[scrape_url],
    prompt="""You are a web content analyst.
From the URLs given, pick the most relevant one and use scrape_url.
Ignore ads, navigation, and noise. Return structured key insights."""
)

# Writer prompt (LLM node, no tools needed)
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior research analyst.
Write detailed, structured, professional research reports.
Ensure logical flow, clear explanations, and real-world relevance."""),
    ("human", """Write a detailed research report.

Topic: {topic}

Research:
{research}

Format:
1. Introduction
2. Key Insights (3-5 detailed points)
3. Real-world Applications
4. Conclusion
5. Sources

Be professional and factual."""),
])
writer_chain = writer_prompt | llm | StrOutputParser()

# Critic prompt (returns a numeric score we can parse)
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict research quality evaluator.
Evaluate reports on: Depth, Clarity, Accuracy, Completeness.
IMPORTANT: Always start your response with 'Score: X/10' on the first line."""),
    ("human", """Evaluate this report:

{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...

Weaknesses:
- ...

Missing Insights:
- ...

Improvement Suggestions:
- ...

Final Verdict:
..."""),
])
critic_chain = critic_prompt | llm | StrOutputParser()