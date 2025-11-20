
from tavily import TavilyClient
import textwrap

print("\n Tavily Research Assistant")
print("------------------------------------------------------------")

query = input("Enter your research query: ").strip()

if not query:
    print("\n A research query is required.")
    exit()

print("\n⏳ Collecting relevant information from the web...\n")


client = TavilyClient(api_key="YOUR API KEY")  


response = client.search(query=query, max_results=3)


print("                    📘 RESEARCH SUMMARY")

print(f"\n Query: {response['query']}")
print("------------------------------------------------------------\n")

print("Top Sources Retrieved:\n")

for idx, item in enumerate(response["results"], start=1):

    print(f"----------------------  SOURCE {idx}  ----------------------")

    title = item.get("title") or "Untitled Source"
    url = item.get("url") or "No URL Available"
    content = item.get("content") or "No content available"

    print(f"Title: {title}")
    print(f"URL: {url}\n")

    print("Content Preview:")
    print(textwrap.fill(content[:600] + "...", width=90))

    print("------------------------------------------------------------\n")


print("Research Completed Successfully")

