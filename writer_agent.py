def writer_node(state, llm):
    """
    Writes a structured academic-style report with clickable reference links.
    """

    topic = state["topic"]
    search_results = state["search_results"]
    length = state["summary_length"]

    style = "very detailed and long" if length == "Detailed" else "short and concise"

    prompt = f"""
    You are an expert Academic Research Writer.

    Write a structured research report on the topic below:

    Topic & Context:
    {topic}

    Verified Online Search Evidence:
    {search_results}

    🎯 Report Format (Follow EXACTLY):
    # {topic}: A Literature Review

    ## 1. Abstract
    - Summary of the full paper in 4-6 sentences.

    ## 2. Key Research Papers & Findings
    - At least 3-5 research findings
    - Each point must include citations in brief text form

    ## 3. Methodologies & Technical Insights
    - Architecture, algorithms, models, techniques used in recent studies

    ## 4. References
    - Add *Clickable Markdown Links* for each reference
    - MUST include valid URLs (Google Scholar / ResearchGate / IEEE / arXiv)
    - Format example:
        - [Paper Title](https://scholar.google.com/link)

    Style: {style}, Fully academic tone.
    Do NOT invent fake titles—use generic titles if needed but MUST give working scholarly links.
    """

    response = llm.invoke(prompt)
    return {"final_report": response.content}

