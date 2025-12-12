🧠 OpenDeepResearcher — AI-Powered Research Assistant
Plan → Search → Synthesize — Automated Academic Report Generator

OpenDeepResearcher is a fully automated AI research workflow built with Streamlit, OpenAI LLMs, and Tavily Search API.
It takes a topic, breaks it into research sub-questions, performs online search, and finally writes a structured academic-style report with:

Abstract

Key Research Papers

Methodologies & Findings

Clickable References (Markdown links)

PDF, Markdown, and JSON downloads

 Features
✅ 1. AI Research Planner

Breaks the user topic into 6–10 structured research questions.

✅ 2. Web Search Agent

For every question, fetches verified online evidence using Tavily Search API.

✅ 3. Academic Writer Agent

Creates a literature-review style report in perfect Markdown format:

# Topic: A Literature Review
## 1. Abstract
## 2. Key Research Papers
## 3. Methodologies & Findings
## 4. References

✅ 4. PDF / Markdown / JSON Export

One-click report downloads.

✅ 5. Memory System

Stores previous research sessions.

✅ 6. Optional PDF Upload

Uploaded PDFs are included in analysis.

🏗️ Project Structure

<img width="662" height="590" alt="image" src="https://github.com/user-attachments/assets/ac57934b-2632-4da5-bd59-9c50d802ecfb" />



🔧 Installation
1️⃣ Clone the repository
git clone https://github.com
cd OpenDeepResearcher

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

🔑 Environment Variables (.env)

Create a .env file:

OPENAI_API_KEY=your_openai_key
OPENAI_API_BASE=https://api.openai.com/v1
TAVILY_API_KEY=your_tavily_key
MODEL_NAME=gpt-4o-mini

▶️ Run the Application
streamlit run app.py


Streamlit will show URLs like:

Local: http://localhost:8501

Network: http://YOUR-IP:8501

🖥️ How It Works (Pipeline)
User Input Topic
       ↓
Planner Agent → Generates research questions  
       ↓
Searcher Agent → Fetches search results  
       ↓
Writer Agent   → Produces Markdown academic report  
       ↓
UI displays + Downloads (PDF/MD/JSON)

📄 Output Example
# Natural Language Processing: A Literature Review

## 1. Abstract
...

## 2. Key Research Papers
- **[Paper Title](URL)** – short description  
...

## 3. Methodologies & Findings
- Transformer models...
- Attention mechanisms...
...

## 4. References
- [Paper Title](URL)
- ...

🐛 Troubleshooting
⚠️ RateLimitError

If OpenAI shows:

429: rate limit reached


Wait 1–2 minutes and try again.

⚠️ Tavily "Query too short"

The planner must generate at least 2-character questions.

⚠️ ImportError (WriterAgent/SearcherAgent)

Ensure file structure and class names exactly match the README.

⭐ Future Enhancements

Multi-agent debate architecture

Auto-summarization of PDFs

Academic reference manager export (BibTeX)

Real-time streaming output

🤝 Contributing

Pull requests are welcome!
Feel free to open issues for improvements or bugs.
