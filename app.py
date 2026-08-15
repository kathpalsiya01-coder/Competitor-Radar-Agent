"""
COMPETITOR RADAR AGENT — Streamlit version
============================================
This wraps the same logic from competitor_radar.py in a simple web page,
so instead of running it from a terminal, you get a live, shareable link.
"""

import os
import streamlit as st

# On Streamlit Cloud, secrets are stored in st.secrets, not a .env file.
# This line makes sure the API key gets set BEFORE we import the functions
# that create the Groq client, so it actually finds the key either way
# (locally from .env, or on Streamlit Cloud from secrets).
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

from competitor_radar import (
    fetch_page_text,
    load_snapshots,
    save_snapshots,
    has_changed,
    summarize_change,
    verify_evidence,
)

st.set_page_config(page_title="Competitor Radar Agent", page_icon="📡")
st.title("📡 Competitor Radar Agent")
st.write(
    "Type a competitor's page — the agent checks it, remembers what it saw "
    "last time, and tells you what changed. Every claim is checked against "
    "the real page text before it's shown as verified."
)

comp_name = st.text_input("Competitor name", value="", placeholder="e.g. Notion")
comp_url = st.text_input(
    "Competitor page URL", value="", placeholder="e.g. https://www.notion.com/pricing"
)

if st.button("Check now", type="primary"):
    if not comp_url:
        st.warning("Please enter a URL first.")
    else:
        with st.spinner(f"Checking {comp_name or comp_url}..."):
            snapshots = load_snapshots()
            new_text = fetch_page_text(comp_url)

            if new_text is None:
                st.error("Could not fetch this page — it may be down or blocking automated requests.")
            else:
                old_text = snapshots.get(comp_url)

                if old_text is None:
                    st.info(
                        f"First check for **{comp_name or comp_url}**. "
                        "Saved as the starting point — run it again later to detect changes."
                    )
                elif has_changed(old_text, new_text):
                    result = summarize_change(comp_name, old_text, new_text)
                    summary = result.get("summary", "")
                    evidence = result.get("evidence", [])

                    if "no meaningful change" in summary.lower():
                        st.success(f"No meaningful change detected for **{comp_name}**.")
                    else:
                        verified, unverified = verify_evidence(evidence, new_text)
                        if verified:
                            st.success(f"✅ Verified change — {comp_name}")
                            st.write(summary)
                            with st.expander("See the exact quotes that prove this"):
                                for q in evidence:
                                    st.caption(f"\"{q}\"")
                        else:
                            st.warning(f"⚠️ Possible change — could not fully verify")
                            st.write(summary)
                            st.caption(f"Could not confirm these quotes on the page: {unverified}")
                else:
                    st.success(f"No change since last check for **{comp_name}**.")

                snapshots[comp_url] = new_text
                save_snapshots(snapshots)

st.divider()
st.caption(
    "How it works: fetches the page → compares it to the last saved version → "
    "asks an LLM to summarize any change → checks the LLM's claim against the "
    "real page text before showing it as verified."
)