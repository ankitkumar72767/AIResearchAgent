from openai import OpenAI
import textwrap

# ---------------------------
# LM STUDIO CONFIGURATION
# ---------------------------
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="test"  
)

print("\n🔎 BASIC RESEARCH AGENT")
print("--------------------------------------------")

topic = input("Enter your research topic: ").strip()

if not topic:
    print("❌ Topic cannot be empty")
    exit()

# ----------------------------------------------
# Step 1 – Generate 3 sub-questions using LLM
# ----------------------------------------------
prompt_subq = f"Generate 3 simple research sub-questions for the topic: {topic}"

subq_resp = client.chat.completions.create(
    model="qwen/qwen2.5-vl-7b",
    messages=[{"role": "user", "content": prompt_subq}]
)

sub_questions = subq_resp.choices[0].message.content
print("\n📌 SUB-QUESTIONS GENERATED:\n")
print(sub_questions)
print("\n--------------------------------------------\n")

# ----------------------------------------------
# Step 2 – Ask LLM to summarize the sub-questions
# ----------------------------------------------
prompt_summary = f"Summarise these sub-questions into one short research paragraph:\n{sub_questions}"

summary_resp = client.chat.completions.create(
    model="qwen/qwen2.5-vl-7b",
    messages=[{"role": "user", "content": prompt_summary}]
)

summary = summary_resp.choices[0].message.content

print("📝 FINAL SUMMARY:\n")
print(textwrap.fill(summary, width=90))

print("\n✔ Research Completed Successfully!\n")
