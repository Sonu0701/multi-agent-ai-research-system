<div align="center">

# 🧠 ResearchMind
### Multi-Agent AI Research System

**An advanced AI system where specialized agents collaborate to search, read, synthesize, and evaluate research — autonomously.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-1C3C3C?style=flat&logo=chainlink&logoColor=white)](https://langchain-ai.github.io/langgraph/)
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

ResearchMind is a **production-style multi-agent AI system** built on **LangGraph** that automates the entire research workflow — from real-time web search to structured report generation — using a graph of specialized AI agents with typed shared state.

Unlike a simple sequential chain, ResearchMind uses a **StateGraph** where each agent reads from and writes to a shared `ResearchState`. The Critic Agent scores every report and automatically loops back to the Writer if quality is below threshold — no human intervention needed.

**Perfect for:**
- 📰 Researching the latest AI/tech trends
- 🔬 Summarizing scientific or academic topics
- 📊 Generating structured reports on any subject
- 🏢 Competitive analysis and market research

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 LangGraph StateGraph | Typed shared state, node-based execution, conditional edges |
| 🔁 Auto-Refinement Loop | Critic scores report — loops back to Writer if score < 7/10 |
| 🌐 Real-time Web Search | Powered by Tavily API — AI-optimized search results |
| 📄 Intelligent Web Scraping | Extracts meaningful content, removes noise via BeautifulSoup |
| ✍️ Structured Report Generation | Coherent, well-organized research reports via Mistral AI |
| 🧐 LLM-as-a-Judge Evaluation | Critic Agent scores reports 1–10 with detailed feedback |
| 🖥️ Live Pipeline UI | Streamlit interface with real-time agent card animations |
| 🧩 Modular Node Design | Each node is independently testable and replaceable |

---

## 🏗️ Architecture

ResearchMind uses a **LangGraph `StateGraph`** — not a sequential chain. Every node reads from and writes to a single typed `ResearchState` object. The Critic node drives a conditional edge that either ends the pipeline or loops the Writer for up to 2 auto-refinement passes.

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│  🔍 search_node                     │
│  Tavily search + URL extraction     │
│  writes: search_results, urls       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  📄 reader_node                     │
│  Scrapes best URL via BeautifulSoup │
│  writes: scraped_content            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐  ◄─────────────────────┐
│  ✍️ writer_node                     │                         │
│  Generates structured report        │  feedback injected      │
│  On retry: uses critic feedback     │  on retry pass          │
│  writes: report                     │                         │
└──────────────────┬──────────────────┘                         │
                   │                                             │
                   ▼                                             │
┌─────────────────────────────────────┐                         │
│  🧐 critic_node                     │                         │
│  LLM evaluates → parses Score: X/10 │                         │
│  writes: feedback, score,           │                         │
│          retry_count                │                         │
└──────────────────┬──────────────────┘                         │
                   │                                             │
                   ▼                                             │
         ┌─────────────────┐   score < 7 AND retry < 2          │
         │  should_retry() │ ──────────────────────────────────►─┘
         └────────┬────────┘
                  │ score ≥ 7 OR retry = 2
                  ▼
         ✅ Final Report + Feedback
```

---

## 🤖 Agents & Nodes

### 🔍 search_node
Runs the **Search Agent** (`create_react_agent`) with the `web_search` tool powered by Tavily API. After the search, it also runs the URL extractor internally — merging what were previously two separate agents into one efficient node. Writes `search_results` and `urls` to state.

### 📄 reader_node
Runs the **Reader Agent** (`create_react_agent`) with the `scrape_url` tool. Picks the most relevant URL from state, scrapes it using `requests` + `BeautifulSoup`, strips boilerplate (navbars, footers, ads), and writes `scraped_content` to state.

### ✍️ writer_node
Runs the **Writer Chain** (Mistral AI via LangChain prompt). On the first pass, it synthesizes search results and scraped content into a structured report. On retry passes (`retry_count > 0`), it additionally injects the Critic's previous feedback so it can address specific weaknesses. Writes `report` to state.

### 🧐 critic_node
Runs the **Critic Chain** (LLM-as-a-judge pattern). Evaluates the report on depth, clarity, accuracy, and completeness. Parses the numeric score from `Score: X/10` in the response. Increments `retry_count`. Writes `feedback`, `score`, and `retry_count` to state.

### 🔀 should_retry() — Conditional Edge
The routing function that drives the refinement loop. If `score < 7` AND `retry_count < 2`, routes back to `writer_node` with the critic's feedback already in state. Otherwise routes to `END`. Maximum 2 retry passes.

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph (StateGraph, conditional edges) |
| LLM Provider | Mistral AI (`mistral-small`) |
| Agent Pattern | `create_react_agent` from `langgraph.prebuilt` |
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
├── agents.py           # Agent and chain definitions (create_react_agent)
├── pipeline.py         # LangGraph StateGraph — nodes, edges, retry logic
├── state.py            # ResearchState TypedDict — shared state schema
├── tools.py            # web_search, scrape_url, extract_urls tools
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
2. Enter a research topic (e.g. *"Latest advancements in quantum computing 2025"*)
3. Click **Run Research Pipeline**
4. Watch each agent card animate live as the graph executes
5. If the Critic scores below 7/10, the Writer automatically retries with feedback
6. Receive your final structured report + Critic evaluation

### Example queries

```
"Explain the impact of AI on healthcare in 2025"
"What are the latest developments in open-source LLMs?"
"Compare React vs Vue.js for enterprise applications"
"Summarize recent breakthroughs in battery technology"
```

---

## 🔑 Key Design Decisions

**Why LangGraph over LangChain sequential chains?**
Sequential chains can only pass outputs forward — there is no way to branch, retry, or loop without writing custom control flow outside the chain. LangGraph's `StateGraph` makes branching a first-class concept via conditional edges. The critic retry loop would be impossible to express cleanly in a plain chain.

**Why merge URL extraction into search_node?**
URL extraction was a 3-line regex operation — not complex enough to justify a dedicated agent, an extra LLM call, and added latency. Merging it into `search_node` keeps the graph minimal and faster.

**Why are Writer and Critic plain chains, not agents?**
They don't need tools — they only need to reason over text. Wrapping them as `create_react_agent` would add a ReAct reasoning loop with no benefit, just extra latency and tokens.

---

## 📸 Screenshots

> 🚧 Screenshots and a live demo link are coming soon.
> **Deploy in progress** — star the repo to stay updated!

---

## 📈 Roadmap

- [x] LangGraph StateGraph orchestration
- [x] Typed shared state (`ResearchState`)
- [x] Conditional critic retry loop (score < 7 → refine)
- [x] Real-time web search via Tavily
- [x] Self-evaluation via Critic Agent (LLM-as-a-judge)
- [x] Live pipeline UI with agent card animations
- [ ] **Async scraping** — parallel URL processing with `asyncio`
- [ ] **Agent memory** — context-aware research across sessions
- [ ] **LangSmith tracing** — full observability on every graph run
- [ ] **Checkpointing** — resume interrupted runs via `MemorySaver`
- [ ] **Live demo deployment** — public Streamlit Cloud link
- [ ] **Docker support** — one-command setup
- [ ] **PDF export** — download report as formatted PDF

---

## 🙋 FAQ

**Q: Do I need a paid API key?**
Both Mistral AI and Tavily offer generous free tiers sufficient to run and test this project.

**Q: Can I use a different LLM like OpenAI or Claude?**
Yes. Swap `ChatMistralAI` for `ChatOpenAI` or `ChatAnthropic` in `agents.py` — the LangGraph graph and all node logic stays identical.

**Q: Why Tavily instead of Google Search?**
Tavily is purpose-built for AI agents — it returns clean, relevance-scored, structured content that LLMs can reason over directly, without the noise of ads and raw HTML.

**Q: What happens if the Critic always scores below 7?**
The pipeline retries the Writer a maximum of 2 times. After that, `should_retry()` routes to `END` regardless of score — preventing infinite loops.

---

## 👨‍💻 Author

**Sonu Kumar**
Final Year B.Tech CS | AI/ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Sonu0701-181717?style=flat&logo=github)](https://github.com/Sonu0701)

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**If this project helped you or impressed you, please give it a ⭐**
It genuinely helps with visibility and motivates further development!

</div>