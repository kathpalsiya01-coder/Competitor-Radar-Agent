<div align="center">

# 📡 Competitor Radar Agent

### An AI agent that watches your competitors — and proves what it tells you.

**Built for [Gravity AI](https://gravity.fast)** · one of Gravity's own use cases, made real: *competitor tracking, as a watch list.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_Demo-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://kathpalsiya01-coder-competitor-radar-agent-app-z8wa8y.streamlit.app/)
[![Groq](https://img.shields.io/badge/LLM-Groq_Llama_3.3-F55036?style=flat)](https://groq.com)
[![Status](https://img.shields.io/badge/Status-Verified_%E2%9C%94-brightgreen?style=flat)](#reliability-not-just-a-demo)

**[🔴 Try the live demo](#)** · **[📖 How it works](#how-it-works)** · **[⚙️ Run it locally](#running-it-locally)**

</div>

---

### 💬 Why I built this for you, Gravity

> *"Use cases include inbox triage, lead follow-up, **competitor tracking**, content scheduling, errand running, **watch lists**, recurring reports... Every agent on the marketplace is gated by 80+ automated quality tests before it ships. **Reliability is the product, not a feature.**"*
> — Gravity AI

I didn't want to build *an idea adjacent to* what Gravity does. I wanted to build the actual thing — one sentence in, an expert-built agent runs, reliability is verifiable, not just claimed. This is that, working end to end.

---

## ✨ What it does

| Step | What happens |
|---|---|
| 1️⃣ **You type one thing** | A competitor's URL. That's the whole input. |
| 2️⃣ **It watches** | Fetches the page, compares it to what it saw last time. |
| 3️⃣ **It explains** | If something changed, an LLM summarizes it in plain English. |
| 4️⃣ **It proves itself** | The LLM must quote its *exact* evidence from the page — and the code independently checks that quote is real before calling anything "verified." |
| 5️⃣ **It reports** | Command line or a live web dashboard — your choice. |

No workflow editor. No integration screen. No step 1, step 2, step 3 for *you* to build — just the outcome.

---

## 🧠 How it works

```
   Your input (one URL)
            │
            ▼
     Fetch the page  ───────►  fails gracefully if the site is down
            │
            ▼
   Compare to last snapshot
            │
     ┌──────┴──────┐
     │             │
  No change     Something changed
     │             │
     ▼             ▼
  Report "OK"   Ask the LLM: summarize it
                    + quote your proof
                    │
                    ▼
        Check every quote against
           the REAL page text
                    │
            ┌───────┴───────┐
            │               │
        Quote found     Quote missing
            │               │
            ▼               ▼
      ✅ VERIFIED      ⚠️ UNVERIFIED
            │               │
            └───────┬───────┘
                     ▼
               Save the report
```

---

## 🛡️ Reliability, not just a demo

Built and tested against real failure cases — not just the happy path Gravity explicitly says they don't want:

- ✅ Target page is a 404 or unreachable → handled gracefully, no crash
- ✅ First-time check on a page → correctly labeled a *baseline*, never a false "change"
- ✅ Nothing meaningfully changed → reported as `OK`, not a false alarm
- ✅ A real change happened → summarized **and** independently verified against the source
- ✅ LLM claims something that isn't actually on the page → flagged `UNVERIFIED`, never trusted blindly

---

## 🛠️ Tech stack

| Layer | Tool |
|---|---|
| Core logic | Python |
| LLM | Groq — `llama-3.3-70b-versatile` |
| Page fetching | Requests + BeautifulSoup |
| Interface | Streamlit |
| Storage | JSON snapshots (lightweight, no DB needed at this scope) |

---

## ⚙️ Running it locally

```bash
# 1. Clone the repo
git clone https://github.com/kathpalsiya01-coder/competitor-radar-agent.git
cd competitor-radar-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
echo GROQ_API_KEY=your_key_here > .env

# 4. Run it
python competitor_radar.py        # command line
streamlit run streamlit_app.py    # or the web dashboard
```

## 📂 Project structure

```
├── competitor_radar.py    # Core agent: fetch, compare, summarize, verify
├── streamlit_app.py       # Web dashboard wrapper
├── requirements.txt       # Dependencies
└── .gitignore              # Keeps API keys out of version control
```

---

## 🚀 What's next

Right now, you tell it which competitors to watch. The natural next step — the one piece deliberately left out of this version — is having the agent **discover relevant competitors on its own** via web search, turning a watch list into a fully autonomous radar.

> I'd rather ship one capability that's bulletproof than five that need a watchful eye. This is the first one, done properly.

<div align="center">

**Made with a lot of curiosity, for Gravity AI — by [Siya Kathpal](https://github.com/kathpalsiya01-coder)**

</div>
