<div align="center">

# 🧠 ResearchMind
### Multi-Agent AI Research System

**An advanced AI system where specialized agents collaborate to search, read, synthesize, and evaluate research — autonomously.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=flat&logo=chainlink&logoColor=white)](https://langchain.com)
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-FF7000?style=flat)](https://mistral.ai)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Tavily](https://img.shields.io/badge/Tavily-Search-4A90E2?style=flat)](https://tavily.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

[Features](#-features) • [Architecture](#-architecture) • [Agents](#-agents) • [Setup](#-setup) • [Usage](#-usage) • [Roadmap](#-roadmap)

---

> 💡 **Deploy in progress** — live demo coming soon. Star the repo to get notified!

</div>

---

## 🔍 What is ResearchMind?

ResearchMind is a **production-style multi-agent AI system** that automates the entire research workflow — from web search to structured report generation — using a pipeline of specialized AI agents.

Instead of a single LLM trying to do everything, ResearchMind assigns each task to a dedicated agent with its own tools and expertise. The result is higher quality, more reliable, and easier to debug than a monolithic LLM approach.

**Perfect for:**
- 📰 Researching the latest AI/tech trends
- 🔬 Summarizing scientific or academic topics
- 📊 Generating structured reports on any subject
- 🏢 Competitive analysis and market research

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 True Multi-Agent Architecture | 5 specialized agents, each with a single responsibility |
| 🌐 Real-time Web Search | Powered by Tavily API — AI-optimized search results |
| 📄 Intelligent Web Scraping | Extracts meaningful content, removes noise |
| ✍️ Structured Report Generation | Coherent, well-organized research reports via Mistral AI |
| 🧐 Self-Evaluation | Critic Agent scores and critiques every report |
| 🖥️ Interactive UI | Clean Streamlit interface — no API knowledge needed |
| 🧩 Modular Design | Each agent is independently testable and replaceable |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Query                         │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  🔍 Search Agent                                        │
│  Fetches real-time results via Tavily API               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  🔗 URL Extractor Agent                                 │
│  Cleans, deduplicates, and validates URLs               │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  📄 Reader Agent                                        │
│  Scrapes pages and extracts key insights                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  ✍️ Writer Chain                                        │
│  Synthesizes content into a structured report           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  🧐 Critic Chain                                        │
│  Evaluates quality — scores, flags gaps, suggests fixes │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│           ✅ Final Research Report + Feedback           │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 Agents

### 🔍 Search Agent
Uses the **Tavily API** — a search engine built for AI agents that returns clean, relevance-scored, structured results instead of raw HTML. Ensures the system always works with up-to-date, real-world information.

### 🔗 URL Extractor Agent
Parses Tavily's response to extract clean, validated URLs. Removes duplicates, invalid links, and redirect noise before passing results downstream. Follows the **Single Responsibility Principle** — isolated for easy testing and maintenance.

### 📄 Reader Agent
Scrapes selected web pages using `requests` + `BeautifulSoup`. Intelligently targets main content areas, strips boilerplate (navbars, footers, ads), and summarizes extracted content to manage LLM context window limits.

### ✍️ Writer Chain 
Powered by **Mistral AI via LangChain**, the Writer takes all gathered insights and generates a coherent, well-structured research report. Uses prompt engineering to enforce consistent report formatting and depth.

### 🧐 Critic Chain
A second LLM instance acting as a quality evaluator (**LLM-as-a-judge** pattern). Scores the report on completeness, coherence, source coverage, and clarity. Returns a numeric score (1–10), identified weaknesses, and concrete improvement suggestions.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| LLM Framework | LangChain |
| LLM Provider | Mistral AI |
| Search | Tavily API |
| Web Scraping | Requests + BeautifulSoup4 |
| Frontend | Streamlit |
| Language | Python 3.10+ |
| Env Management | python-dotenv |

---

## 📂 Project Structure

```
multi-agent-ai-research-system/
│
├── app.py              # Streamlit UI — entry point
├── agents.py           # Agent definitions and prompts
├── tools.py            # Search, scraping, URL extraction tools
├── pipeline.py         # Multi-agent workflow orchestration
├── requirements.txt    # Dependencies
└── .env.example        # Environment variable template
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.10+
- A [Mistral AI API key](https://console.mistral.ai/) (free tier works)
- A [Tavily API key](https://tavily.com/) (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/Sonu0701/multi-agent-ai-research-system.git
cd multi-agent-ai-research-system
```

### 2. Create a virtual environment

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Or using standard venv
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
# Using uv
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` 🚀

---

## 🚀 Usage

1. Open the Streamlit UI in your browser
2. Enter a research topic in the input field (e.g., *"Latest advancements in quantum computing 2025"*)
3. Click **Run Research**
4. Watch each agent work through the pipeline in real time
5. Receive your structured report + Critic Agent's quality evaluation

### Example queries

```
"Explain the impact of AI on healthcare in 2025"
"What are the latest developments in open-source LLMs?"
"Compare React vs Vue.js for enterprise applications"
"Summarize recent breakthroughs in battery technology"
```

---

## 📸 Screenshots

> 🚧 Screenshots and a live demo link are coming soon.
> **Deploy in progress** — star the repo to stay updated!

---

## 📈 Roadmap

- [x] Sequential multi-agent pipeline
- [x] Real-time web search via Tavily
- [x] Self-evaluation via Critic Agent
- [x] Streamlit UI
- [ ] **LangGraph orchestration** — conditional branching & auto-refinement loops
- [ ] **Async scraping** — parallel URL processing with `asyncio`
- [ ] **Agent memory** — context-aware research across sessions
- [ ] **Live demo deployment** — public Streamlit Cloud link
- [ ] **Docker support** — one-command setup
- [ ] **Report export** — download as PDF or Markdown

---

## 🙋 FAQ

**Q: Do I need a paid API key?**
Both Mistral AI and Tavily offer generous free tiers that are sufficient to run and test this project.

**Q: Can I use a different LLM like OpenAI or Claude?**
Yes. Because the system is built on LangChain, swapping the LLM provider requires changing only a few lines in `agents.py`. GPT-4o or Claude Sonnet would work as drop-in replacements.

**Q: Why Tavily instead of Google Search?**
Tavily is purpose-built for AI agents — it returns clean, relevance-scored, structured content that LLMs can reason over directly, without the noise of ads, navigation, and raw HTML that comes from scraping Google results.

---

## 👨‍💻 Author

**Sonu Kumar**
Final Year Student | AI/ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Sonu0701-181717?style=flat&logo=github)](https://github.com/Sonu0701)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**If this project helped you or impressed you, please give it a ⭐**
It genuinely helps with visibility and motivates further development!

</div>