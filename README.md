📡 Competitor Radar Agent

An AI agent that watches a competitor's webpage, tells you what changed in plain English, and proves it by checking every claim against the real page text before calling it verified.

Live demo: [add your Streamlit Cloud link here after deploying] Built by: Siya Kathpal

Why this project

"Use cases include inbox triage, lead follow-up, competitor tracking, content scheduling, errand running, watch lists, recurring reports... Every agent on the marketplace is gated by 80+ automated quality tests before it ships. Reliability is the product, not a feature." — Gravity AI

This project is a direct, working implementation of one of Gravity's own named use cases — competitor tracking as a watch list — built around the same core philosophy: an agent's output is only as good as your ability to trust it. So instead of just asking an LLM to summarize a change and hoping it's right, this agent makes the LLM show its work, then checks that work in code before it's ever shown to you as fact.

What it does
You type one thing: a competitor's URL (and a name, for readability).
It fetches the page and compares the text to what it saw last time.
If something changed, an LLM summarizes it in plain English — and is required to back up the summary with exact, word-for-word quotes from the page.
The code independently verifies each quote actually exists in the real page text. Only then is a change marked VERIFIED. If a quote can't be confirmed, it's flagged UNVERIFIED instead of silently trusted.
A report is generated, either from the command line or a live web dashboard.

No configuration, no workflow builder — one input, one output, matching the "no setup, no fine-tuning" philosophy behind Gravity's own product.

How it works
User input (competitor URL)
        │
        ▼
   Fetch page text  ──────► (fails gracefully if site is down/blocking)
        │
        ▼
Compare to last saved snapshot
        │
   ┌────┴────┐
   │ No       │ Yes
   │ change   │
   ▼          ▼
 Report    Ask LLM for a summary + supporting quotes
 "OK"           │
                ▼
     Check each quote against the real page text
                │
        ┌───────┴───────┐
        │ Found          │ Not found
        ▼                ▼
   Mark VERIFIED     Mark UNVERIFIED
        │                │
        └───────┬────────┘
                ▼
          Save report
Reliability, not just a demo

Built and tested against real failure cases, not just the happy path:

✅ Target page returns a 404 or is otherwise unreachable — handled without crashing
✅ First-time check on a page (no prior snapshot) — correctly labeled as a baseline, not falsely reported as a "change"
✅ No meaningful change between checks — correctly reported as OK, not a false alarm
✅ Real detected change — summarized and independently verified against the source page
✅ LLM claim that can't be confirmed on the page — flagged UNVERIFIED rather than trusted blindly
Tech stack
Python — core logic
Groq API (llama-3.3-70b-versatile) — LLM summarization
BeautifulSoup + Requests — page fetching and text extraction
Streamlit — live web interface
JSON — lightweight snapshot storage (no database needed for this scope)
Running it locally
bash
# 1. Clone the repo
git clone https://github.com/kathpalsiya01-coder/competitor-radar-agent.git
cd competitor-radar-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
# Create a .env file in the project root:
echo GROQ_API_KEY=your_key_here > .env

# 4a. Run from the command line
python competitor_radar.py

# 4b. Or run the web dashboard
streamlit run streamlit_app.py
Project structure
├── competitor_radar.py    # Core agent logic: fetch, compare, summarize, verify
├── streamlit_app.py       # Web dashboard wrapper around the same logic
├── requirements.txt       # Dependencies
└── .gitignore              # Keeps API keys and local env out of version control
What's next

The current version tracks competitors you name directly. The natural next step is having the agent discover relevant competitors on its own via web search, rather than requiring them as input — turning this from a watch list into a fully autonomous radar. Deliberately left out of this version to ship something reliable first, rather than something broad and untested.

Note on scope

This was built as a focused, honest demonstration of one capability done well — not a claim of feature completeness. The goal was to show working, verifiable reliability on a real use case, in the spirit of "ship five capabilities that are bulletproof" over "fifty that need a watchful eye."
