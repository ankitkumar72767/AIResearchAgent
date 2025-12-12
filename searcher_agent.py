def searcher_node(state, tavily_client):
    """
    Executes the search plan using Tavily and returns
    a nicely formatted markdown string of combined results.

    Args:
        state: AgentState
        tavily_client: The initialized TavilyClient

    Returns:
        dict with key "search_results" -> str (markdown)
    """
    queries = state.get("research_plan") or []
    all_sections = []

    if not queries:
        # In case planner failed or empty
        return {
            "search_results": "No research queries were generated. Please try refining the topic."
        }

    for idx, q in enumerate(queries, start=1):
        try:
            # "advanced" gives deeper results; you can change to "basic" if you want cheaper/faster
            response = tavily_client.search(
                query=q,
                max_results=3,
                search_depth="advanced",
            )

            results = response.get("results", [])

            if not results:
                section = f"### Source {idx}: {q}\n_No data found from web search._"
                all_sections.append(section)
                continue

            # Build markdown for this query
            section_lines = [f"### Source {idx}: {q}"]

            for r_idx, item in enumerate(results, start=1):
                title = item.get("title") or f"Result {r_idx}"
                url = item.get("url") or ""
                content = item.get("content") or ""
                snippet = content.strip()

                # Optional: truncate overly long snippet
                if len(snippet) > 1200:
                    snippet = snippet[:1200] + "..."

                line = f"- **{title}**\n"
                if url:
                    line += f"  - URL: {url}\n"
                line += f"  - Notes: {snippet}\n"

                section_lines.append(line)

            all_sections.append("\n".join(section_lines))

        except Exception as e:
            error_section = (
                f"### Source {idx}: {q}\n"
                f"_Error while searching this query:_ `{e}`"
            )
            all_sections.append(error_section)

    combined_content = "\n\n".join(all_sections)
    return {"search_results": combined_content}
