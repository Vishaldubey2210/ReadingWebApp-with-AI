"""
==========================================================
ReadingAI - Result Dashboard
Author : Vishal Kumar
==========================================================
"""

import json
import io
import streamlit as st
from pathlib import Path

from core.scoring import ReadingResult


# ── Colour palette (matches app theme) ─────────────────────────────────
_CLR_CORRECT     = "#16a34a"
_CLR_SUBSTITUTED = "#f59e0b"
_CLR_SKIPPED     = "#dc2626"
_CLR_INSERTED    = "#2563eb"
_CLR_BG_CARD     = "#1e293b"

# Status → (emoji, hex colour, Streamlit CSS override via markdown)
_STATUS_META = {
    "correct":     ("✅", _CLR_CORRECT,     "green"),
    "substituted": ("🔄", _CLR_SUBSTITUTED, "orange"),
    "skipped":     ("❌", _CLR_SKIPPED,     "red"),
    "inserted":    ("➕", _CLR_INSERTED,    "blue"),
}


def _pct_bar(label: str, value: float, color: str) -> None:
    """Renders a labelled progress bar with value text."""
    col_l, col_bar = st.columns([1, 4])
    with col_l:
        st.markdown(f"**{label}**")
    with col_bar:
        st.progress(min(value / 100, 1.0))
    st.caption(f"{value:.1f}%")


def _metric_card(col, label: str, value: str, delta: str = "", color: str = "") -> None:
    with col:
        st.metric(label=label, value=value, delta=delta or None)



def show_dashboard() -> None:
    """
    Renders the full result dashboard.
    Reads from st.session_state["result"].
    """
    result: ReadingResult = st.session_state.get("result")
    if result is None:
        st.warning("No result available yet. Complete a reading session first.")
        if st.button("⬅ Back to Reading"):
            st.session_state.show_dashboard = False
            st.rerun()
        return

    st.title("📊 Reading Result Dashboard")
    st.caption(f"Article: **{result.article_title or result.article_id}**")
    st.divider()

    # ── Top KPI metrics ───────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    _metric_card(c1, "🎯 Accuracy",       f"{result.accuracy:.1f}%")
    _metric_card(c2, "⚡ Reading Speed",   f"{result.wpm:.0f} WPM")
    _metric_card(c3, "⏱ Reading Time",    f"{result.reading_time_sec:.1f}s")
    _metric_card(c4, "📝 Total Words",     str(result.total_words))

    st.divider()

    # ── Progress bars ──────────────────────────────────────────────────
    st.subheader("Word Accuracy Breakdown")
    total = result.total_words or 1
    _pct_bar("✅ Correct",     result.correct_words     / total * 100, _CLR_CORRECT)
    _pct_bar("🔄 Substituted", result.substituted_words / total * 100, _CLR_SUBSTITUTED)
    _pct_bar("❌ Skipped",     result.skipped_words     / total * 100, _CLR_SKIPPED)
    _pct_bar("➕ Inserted",    result.inserted_words    / total * 100, _CLR_INSERTED)

    st.divider()

    # ── Transcript ─────────────────────────────────────────────────────
    transcript = getattr(result, "transcript", None) or result.__dict__.get("transcript", "")
    if transcript:
        st.subheader("🎙 Transcription")
        st.markdown(f"> {transcript}")
        st.divider()

    # ── Word-by-word table ────────────────────────────────────────────
    st.subheader("🔍 Word-by-Word Analysis")
    if result.alignments:
        rows = []
        for a in result.alignments:
            emoji, hex_color, _ = _STATUS_META.get(a.status, ("❓", "#666", "grey"))
            rows.append({
                "#":         a.index + 1,
                "Expected":  a.expected,
                "Spoken":    a.spoken if a.spoken else "—",
                "Status":    f"{emoji} {a.status.capitalize()}",
                "Score":     f"{a.similarity:.0f}",
            })
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No alignment data available.")

    # ── Inserted words ─────────────────────────────────────────────────
    if result.inserted_word_list:
        st.subheader("➕ Extra Words Spoken")
        st.markdown("  ".join(
            f"`{w}`" for w in result.inserted_word_list
        ))

    st.divider()

    # ── Downloads ─────────────────────────────────────────────────────
    st.subheader("⬇ Download Report")
    col_json, col_pdf, col_back = st.columns(3)

    with col_json:
        json_bytes = json.dumps(result.to_dict(), indent=2, ensure_ascii=False).encode("utf-8")
        st.download_button(
            "📄 Download JSON",
            data=json_bytes,
            file_name=f"result_{result.article_id}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col_pdf:
        st.info("PDF download is disabled in the cloud version.")

    with col_back:
        if st.button("⬅ Back to Reading", use_container_width=True):
            st.session_state.show_dashboard = False
            st.rerun()
