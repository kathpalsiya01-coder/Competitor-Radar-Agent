"""
COMPETITOR RADAR AGENT - Step 1 version
========================================
What this does, in plain words:
1. You give it a list of competitor pages to watch.
2. It downloads each page and reads the text.
3. It compares today's text to what it saw last time (saved in a small file).
4. If something changed, it asks an AI to explain the change in plain English.
5. It saves a report and prints it.

Run it once to create a baseline, then run it again later to see changes.
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from groq import Groq  # pip install groq
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()  # reads the .env file in the same folder and loads its values

# ============================================
# SETTINGS — change these for your own project
# ============================================

MY_PRODUCT = "MyApp"  # your product/company name, just for the report title

COMPETITORS = [
    {"name": "Notion", "url": "https://www.notion.com/pricing"},
    {"name": "Airtable", "url": "https://www.airtable.com/pricing"},
]

SNAPSHOT_FILE = "competitor_snapshots.json"  # the agent's "notebook" of what it saw last time
REPORT_FILE = "competitor_report.txt"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


# ============================================
# STEP A: FETCH — go get the competitor's page text
# ============================================

def fetch_page_text(url):
    """Downloads a webpage and pulls out just the readable text (no HTML tags).
    Returns None if the site is down or blocks us — we handle that gracefully,
    not by crashing."""
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style"]):  # scripts/styles aren't real content
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"  Could not fetch this page: {e}")
        return None


# ============================================
# STEP B: REMEMBER — load/save what the agent saw last time
# ============================================

def load_snapshots():
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_snapshots(snapshots):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshots, f, indent=2)


# ============================================
# STEP C: COMPARE — has anything actually changed?
# ============================================

def has_changed(old_text, new_text):
    if old_text is None:
        return True  # first time seeing this page — treat it as "new" (baseline)
    return old_text.strip() != new_text.strip()


# ============================================
# STEP D: EXPLAIN — ask the AI to summarize the change, AND give us proof
# We only ever give it real text from the page — it is NOT allowed to guess.
# ============================================

def summarize_change(competitor_name, old_text, new_text):
    prompt = f"""You are comparing two versions of a competitor's webpage text for {competitor_name}.

OLD VERSION:
{old_text[:3000] if old_text else "(no earlier version - this is the first check, so just summarize what's on the page now)"}

NEW VERSION:
{new_text[:3000]}

Task: Describe what meaningfully changed (pricing, features, plans) in 2-3 plain English sentences.

Respond ONLY in this exact JSON format, nothing else, no markdown fences:
{{
  "summary": "your 2-3 sentence summary here",
  "evidence": ["exact word-for-word quote copied from NEW VERSION that proves this", "another exact quote if needed"]
}}

Rules:
- Each evidence quote must be copied EXACTLY, word-for-word, from the NEW VERSION text above. Do not paraphrase the quotes.
- If nothing meaningful changed, respond with: {{"summary": "No meaningful change detected.", "evidence": []}}
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # if the AI didn't format it properly, fall back to treating it as unverifiable
        return {"summary": raw, "evidence": []}


# ============================================
# STEP D.5: VERIFY — check the AI's quotes actually exist on the real page
# This is what turns "verifies sources" from a buzzword into something true.
# ============================================

def verify_evidence(evidence_list, source_text):
    """Checks each evidence quote actually appears in the real page text.
    Returns (all_verified, list_of_quotes_that_could_not_be_found)."""
    source_lower = source_text.lower()
    unverified = [q for q in evidence_list if q.strip() and q.strip().lower() not in source_lower]
    return (len(unverified) == 0), unverified


# ============================================
# STEP E: RUN EVERYTHING
# ============================================

def run_competitor_radar():
    snapshots = load_snapshots()
    report_lines = [f"Competitor Radar Report for {MY_PRODUCT}", f"Generated: {datetime.now()}", ""]
    any_changes = False

    for comp in COMPETITORS:
        name, url = comp["name"], comp["url"]
        print(f"Checking {name}...")
        new_text = fetch_page_text(url)

        if new_text is None:
            report_lines.append(f"[!] {name}: Could not fetch page (site down or blocking us)")
            continue

        old_text = snapshots.get(url)

        if old_text is None:
            # first time ever seeing this page - nothing to compare against yet
            report_lines.append(f"[BASELINE] {name}: First check - saved as starting point")
        elif has_changed(old_text, new_text):
            result = summarize_change(name, old_text, new_text)
            summary = result.get("summary", "")
            evidence = result.get("evidence", [])

            if "no meaningful change" in summary.lower():
                report_lines.append(f"[OK] {name}: No meaningful change since last check")
            else:
                any_changes = True
                verified, unverified_quotes = verify_evidence(evidence, new_text)
                if verified:
                    report_lines.append(f"[CHANGED - VERIFIED] {name}: {summary}")
                else:
                    report_lines.append(
                        f"[CHANGED - UNVERIFIED] {name}: {summary} "
                        f"(could not confirm these quotes on the page: {unverified_quotes} — double-check manually)"
                    )
        else:
            report_lines.append(f"[OK] {name}: No change since last check")

        snapshots[url] = new_text  # update the notebook for next time

    save_snapshots(snapshots)

    report_text = "\n".join(report_lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report_text)

    print("\n" + report_text)

    if any_changes:
        print(f"\nReport saved to {REPORT_FILE} — something changed, go check it.")
    else:
        print(f"\nNo changes this run. Report saved to {REPORT_FILE} anyway.")


if __name__ == "__main__":
    run_competitor_radar()