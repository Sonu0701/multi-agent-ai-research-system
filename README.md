# 🔬 ResearchMind — Multi-Agent AI Research System

> An advanced AI system where multiple intelligent agents collaborate to perform deep research, analyze information, and generate structured reports.

---

## 🧠 Overview

**ResearchMind** is a production-style **Multi-Agent AI System** built using modern LLM frameworks.
It simulates how a team of specialized AI agents can work together to solve complex research problems.

Instead of a single LLM response, this system uses **agent collaboration + tool usage + structured workflows** to produce high-quality outputs.

---

## ⚙️ System Architecture

```text
User Query
    ↓
🔍 Search Agent (Tavily API)
    ↓
🔗 URL Extractor Agent
    ↓
📄 Reader Agent (Web Scraper)
    ↓
✍️ Writer Agent (LLM)
    ↓
🧐 Critic Agent (LLM Evaluation)
    ↓
Final Research Report + Feedback
```

---

## 🤖 Agents in the System

### 🔍 Search Agent

* Fetches real-time web data using Tavily API
* Ensures relevant and recent information

### 🔗 URL Extractor Agent

* Extracts clean URLs from raw search results
* Removes noise and duplicates

### 📄 Reader Agent

* Scrapes selected web pages
* Extracts meaningful insights

### ✍️ Writer Agent

* Generates structured research reports
* Uses context from multiple sources

### 🧐 Critic Agent

* Evaluates report quality
* Provides score, feedback, and improvements

---

## 🚀 Features

* ✅ True Multi-Agent Architecture
* ✅ Tool-based reasoning (Search + Scraping)
* ✅ Streamlit UI (Modern & Interactive)
* ✅ Structured Research Reports
* ✅ Self-evaluation using Critic Agent
* ✅ Modular & Scalable Design

---

## 🧰 Tech Stack

* **LLM Framework:** LangChain
* **LLM Provider:** Mistral AI
* **Search Tool:** Tavily API
* **Frontend:** Streamlit
* **Backend:** Python

---

## 📸 UI Preview

> Add screenshots here (VERY IMPORTANT for recruiters)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/multi-agent-ai-research-system.git
cd multi-agent-ai-research-system
```

### 2️⃣ Create virtual environment

```bash
uv venv
.venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
uv pip install -r requirements.txt
```

### 4️⃣ Create `.env` file

```env
MISTRAL_API_KEY=your_mistral_key
TAVILY_API_KEY=your_tavily_key
```

### 5️⃣ Run the application

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
├── app.py          # Streamlit UI
├── agents.py       # Agent definitions
├── tools.py        # Tools (search, scraping, URL extraction)
├── pipeline.py     # Multi-agent workflow
├── requirements.txt
└── .env
```

---

## 🧪 Example Use Cases

* Research latest AI trends
* Analyze scientific topics
* Generate structured reports
* Evaluate content quality

---

## 📈 Future Improvements

* 🔥 LangGraph-based orchestration
* 🧠 Memory (context-aware agents)
* 🔁 Self-improving loop (auto-refinement)
* 🌐 Deployment (public demo link)

---

## 👨‍💻 Author

**Sonu Kumar**
Final Year Student | AI/ML Enthusiast

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
