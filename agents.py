from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url, extract_urls
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

if not os.getenv("MISTRAL_API_KEY"):
    raise ValueError("MISTRAL_API_KEY missing")

# LLM setup
llm = ChatMistralAI(
    model="mistral-small",
    temperature=0.2
)

# ==============================
# 🔍 SEARCH AGENT
# ==============================
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt="""
You are a research search specialist.

Your responsibilities:
- Search for accurate, recent, and relevant information
- Use the web_search tool whenever needed
- Return structured results with titles, URLs, and summaries

Rules:
- Always prefer trusted sources
- Focus on clarity and relevance
- Do NOT hallucinate
"""
    )

# ==============================
# 🔗 URL EXTRACTOR AGENT
# ==============================
def build_url_extractor_agent():
    return create_agent(
        model=llm,
        tools=[extract_urls],
        system_prompt="""
You are a URL extraction assistant.

Your job:
- Extract all valid URLs from the given text
- Remove duplicates
- Return only clean URLs

Do NOT add extra explanation.
"""
    )

# ==============================
# 📄 READER AGENT
# ==============================
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt="""
You are a web content analyst.

Your job:
- Read and extract useful information from web pages
- Ignore ads, navigation, and noise
- Focus on key insights, facts, and explanations

Instructions:
- Use scrape_url tool with the best URL
- Return structured insights
"""
    )

# ==============================
# ✍️ WRITER CHAIN
# ==============================
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a senior research analyst.

Write detailed, structured, and professional research reports.
Ensure:
- Logical flow
- Clear explanations
- Real-world relevance
"""),

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

# ==============================
# 🧠 CRITIC CHAIN
# ==============================
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict research evaluator.

Evaluate based on:
- Depth
- Clarity
- Accuracy
- Completeness
"""),

    ("human", """Evaluate this report:

{report}

Give output in format:

Score: X/10

Strengths:
- ...

Weaknesses:
- ...

Missing Insights:
- ...

Final Verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()