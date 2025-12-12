def planner_node(state, llm):
    """
    Analyze the user's topic/context and generate focused web-search queries.

    Args:
        state: AgentState  -> contains 'topic' and other fields
        llm:   ChatOpenAI or any LangChain compatible LLM (OpenAI / OpenRouter)

    Returns:
        dict with key 'research_plan' -> List[str] of up to 3 search queries
    """
    topic = state["topic"]

    # Optional: avoid sending extremely long context directly as-is
    if len(topic) > 4000:
        topic_snippet = topic[:4000] + "... [truncated]"
    else:
        topic_snippet = topic

    prompt = f"""
You are an expert Research Planner for a multi-agent research system.

User Topic / Context:
\"\"\"{topic_snippet}\"\"\"


Your job:
1. Break this into 3 focused web-search queries.
2. Each query should be specific, non-overlapping, and help build a deep report.
3. Cover:
   - background / fundamentals
   - recent developments / current state
   - applications, challenges, or comparisons

VERY IMPORTANT:
- Return ONLY the 3 queries.
- Put each query on a NEW LINE.
- Do NOT add numbers, bullets, explanations, or any extra text.
"""

    # ---- Call LLM (works for ChatGPT / OpenRouter through ChatOpenAI) ----
    response = llm.invoke(prompt)

    # response may be an AIMessage; ensure we convert to text safely
    text = getattr(response, "content", str(response))

    # Split into lines, clean up, remove empty lines
    raw_lines = text.split("\n")
    queries = [line.strip() for line in raw_lines if line.strip()]

    # Ensure we only return max 3 queries, and if somehow LLM failed, fall back.
    if not queries:
        # basic safe fallback in case model returns nothing usable
        queries = [
            f"{topic} overview and fundamentals",
            f"recent research and developments on {topic}",
            f"real-world applications, challenges, and future trends of {topic}",
        ]

    return {"research_plan": queries[:3]}
