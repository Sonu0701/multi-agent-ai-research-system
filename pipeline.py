from agents import (
    build_reader_agent,
    build_search_agent,
    build_url_extractor_agent,
    writer_chain,
    critic_chain
)

def log_step(step):
    print(f"\n{'='*20} {step} {'='*20}")


def run_research_pipeline(topic: str) -> dict:

    state = {
        "topic": topic,
        "search_results": "",
        "urls": "",
        "scraped_content": "",
        "report": "",
        "feedback": ""
    }

    # ==========================
    # STEP 1: SEARCH
    # ==========================
    log_step("STEP 1 - SEARCH AGENT")

    try:
        search_agent = build_search_agent()

        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent and detailed information about: {topic}")]
        })

        state["search_results"] = search_result['messages'][-1].content

        print("\n🔍 Search Results:\n", state["search_results"])

    except Exception as e:
        print("❌ Search Error:", e)
        state["search_results"] = "No results"


    # ==========================
    # STEP 2: URL EXTRACTION
    # ==========================
    log_step("STEP 2 - URL EXTRACTION AGENT")

    try:
        url_agent = build_url_extractor_agent()

        url_result = url_agent.invoke({
            "messages": [("user", f"Extract all URLs from this text:\n{state['search_results']}")]
        })

        state["urls"] = url_result['messages'][-1].content

        print("\n🔗 Extracted URLs:\n", state["urls"])

    except Exception as e:
        print("❌ URL Extraction Error:", e)
        state["urls"] = ""


    # ==========================
    # STEP 3: READER (SCRAPE BEST URL)
    # ==========================
    log_step("STEP 3 - READER AGENT")

    try:
        reader_agent = build_reader_agent()

        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"From these URLs, choose the most relevant one and extract insights:\n{state['urls']}"
            )]
        })

        state["scraped_content"] = reader_result['messages'][-1].content

        print("\n📄 Scraped Content:\n", state["scraped_content"])

    except Exception as e:
        print("❌ Reader Error:", e)
        state["scraped_content"] = "No content"


    # ==========================
    # STEP 4: WRITER
    # ==========================
    log_step("STEP 4 - WRITER AGENT")

    try:
        combined = f"""
        SEARCH RESULTS:
        {state['search_results']}

        SCRAPED CONTENT:
        {state['scraped_content']}
        """

        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": combined
        })

        print("\n📝 Generated Report:\n", state["report"])

    except Exception as e:
        print("❌ Writer Error:", e)
        state["report"] = "Failed to generate report"


    # ==========================
    # STEP 5: CRITIC
    # ==========================
    log_step("STEP 5 - CRITIC AGENT")

    try:
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })

        print("\n🧠 Critic Feedback:\n", state["feedback"])

    except Exception as e:
        print("❌ Critic Error:", e)
        state["feedback"] = "No feedback"


    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    result = run_research_pipeline(topic)

    print("\n" + "="*60)
    print("✅ FINAL OUTPUT")
    print("="*60)
    print("\nREPORT:\n", result["report"])
    print("\nFEEDBACK:\n", result["feedback"])