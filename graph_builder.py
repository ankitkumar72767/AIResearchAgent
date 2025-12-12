from functools import partial
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from state import AgentState
from planner_agent import planner_node
from searcher_agent import searcher_node
from writer_agent import writer_node


def build_graph(provider: str, openrouter_api_key: str, openai_api_key: str, tavily_api_key: str):
    """
    Initialize LLM (ChatGPT or OpenRouter) + Tavily and build the LangGraph workflow.
    provider: "openrouter" | "openai"
    """

    # ---------- LLM SELECTION ----------
    if provider == "openai":
        # Direct ChatGPT (OpenAI) usage
        llm = ChatOpenAI(
            model="gpt-4.1-mini",   # you can change to gpt-4.1, gpt-4o, etc. if you have access
            openai_api_key=openai_api_key,
            temperature=0.5,
        )
    else:
        # OpenRouter (proxy for Gemini / GPT etc.)
        llm = ChatOpenAI(
            model="google/gemini-2.0-flash-001",  # or "openai/gpt-4o-mini" via OpenRouter
            openai_api_key=openrouter_api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.5,
        )

    # ---------- Tavily Client ----------
    tavily = TavilyClient(api_key=tavily_api_key)

    # ---------- Wrap Nodes with dependencies ----------
    p_node = partial(planner_node, llm=llm)
    s_node = partial(searcher_node, tavily_client=tavily)
    w_node = partial(writer_node, llm=llm)

    # ---------- Build LangGraph ----------
    workflow = StateGraph(AgentState)

    workflow.add_node("planner", p_node)
    workflow.add_node("searcher", s_node)
    workflow.add_node("writer", w_node)

    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
