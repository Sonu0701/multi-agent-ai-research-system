from langgraph.graph import StateGraph, END
from state import ResearchState
from agents import (
    search_agent, url_agent, reader_agent,
    writer_chain, critic_chain
)
import re

MAX_RETRIES = 2

# ──────────────────────────────────────────────
# NODE FUNCTIONS
# ──────────────────────────────────────────────

def search_node(state: ResearchState) -> dict:
    """Runs search agent then URL extractor — merged for efficiency."""
    print("\n[search_node] Running...")
    try:
        result = search_agent.invoke({
            "messages": [("user", f"Find recent detailed information about: {state['topic']}")]
        })
        search_out = result["messages"][-1].content

        url_result = url_agent.invoke({
            "messages": [("user", f"Extract all URLs from this text:\n{search_out}")]
        })
        urls_out = url_result["messages"][-1].content

        return {"search_results": search_out, "urls": urls_out}
    except Exception as e:
        print(f"[search_node] Error: {e}")
        return {"search_results": "No results", "urls": ""}


def reader_node(state: ResearchState) -> dict:
    """Scrapes the best URL from extracted URLs."""
    print("\n[reader_node] Running...")
    try:
        result = reader_agent.invoke({
            "messages": [("user",
                f"From these URLs, pick the most relevant and extract insights:\n{state['urls']}"
            )]
        })
        return {"scraped_content": result["messages"][-1].content}
    except Exception as e:
        print(f"[reader_node] Error: {e}")
        return {"scraped_content": "No content"}


def writer_node(state: ResearchState) -> dict:
    """Generates the research report. Uses previous feedback if retrying."""
    print(f"\n[writer_node] Running... (retry #{state.get('retry_count', 0)})")
    try:
        combined = f"SEARCH RESULTS:\n{state['search_results']}\n\nSCRAPED CONTENT:\n{state['scraped_content']}"

        if state.get("feedback") and state.get("retry_count", 0) > 0:
            combined += f"\n\nPREVIOUS FEEDBACK TO IMPROVE ON:\n{state['feedback']}"

        report = writer_chain.invoke({"topic": state["topic"], "research": combined})
        return {"report": report}
    except Exception as e:
        print(f"[writer_node] Error: {e}")
        return {"report": "Failed to generate report"}


def critic_node(state: ResearchState) -> dict:
    """Evaluates the report and extracts a numeric score."""
    print("\n[critic_node] Running...")
    try:
        feedback = critic_chain.invoke({"report": state["report"]})

        match = re.search(r"Score:\s*(\d+)/10", feedback, re.IGNORECASE)
        score = int(match.group(1)) if match else 5

        print(f"[critic_node] Score: {score}/10")
        return {
            "feedback": feedback,
            "score": score,
            "retry_count": state.get("retry_count", 0) + 1
        }
    except Exception as e:
        print(f"[critic_node] Error: {e}")
        return {"feedback": "No feedback", "score": 5, "retry_count": 1}

# ──────────────────────────────────────────────
# CONDITIONAL EDGE — retry logic
# ──────────────────────────────────────────────

def should_retry(state: ResearchState) -> str:
    """If score < 7 and retries remaining, loop back to writer."""
    score = state.get("score", 5)
    retries = state.get("retry_count", 0)

    if score < 7 and retries < MAX_RETRIES:
        print(f"\n[router] Score {score}/10 < 7. Retrying writer... ({retries}/{MAX_RETRIES})")
        return "retry"
    else:
        print(f"\n[router] Score {score}/10. Pipeline complete.")
        return "done"


# ──────────────────────────────────────────────
# BUILD THE GRAPH
# ──────────────────────────────────────────────

def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_node)
    graph.add_node("reader", reader_node)
    graph.add_node("writer", writer_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("search")
    graph.add_edge("search", "reader")
    graph.add_edge("reader", "writer")
    graph.add_edge("writer", "critic")

    graph.add_conditional_edges(
        "critic",
        should_retry,
        {
            "retry": "writer",
            "done":  END
        }
    )

    return graph.compile()


# For direct testing
if __name__ == "__main__":
    app = build_research_graph()
    topic = input("Enter research topic: ")

    final_state = app.invoke({
        "topic": topic,
        "search_results": "",
        "scraped_content": "",
        "report": "",
        "feedback": "",
        "score": 0,
        "retry_count": 0,
        "urls": ""
    })

    print("\n" + "="*60)
    print("FINAL REPORT:\n", final_state["report"])
    print("\nFINAL FEEDBACK:\n", final_state["feedback"])
    print(f"\nFINAL SCORE: {final_state['score']}/10")