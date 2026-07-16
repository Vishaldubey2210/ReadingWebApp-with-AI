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

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable,
)

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


def _build_pdf(result: ReadingResult) -> bytes:
    """Generates a PDF report using reportlab and returns raw bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = ParagraphStyle("Title", parent=styles["Title"],
                                 fontSize=20, spaceAfter=6)
    elements.append(Paragraph("📖 ReadingAI — Session Report", title_style))
    elements.append(Paragraph(f"Article: <b>{result.article_title or result.article_id}</b>",
                               styles["Normal"]))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    elements.append(Spacer(1, 0.4*cm))

    # Summary table
    summary_data = [
        ["Metric", "Value"],
        ["Accuracy",          f"{result.accuracy:.1f}%"],
        ["Reading Speed",     f"{result.wpm:.0f} WPM"],
        ["Reading Time",      f"{result.reading_time_sec:.1f} s"],
        ["Total Words",       str(result.total_words)],
        ["Correct Words",     str(result.correct_words)],
        ["Skipped Words",     str(result.skipped_words)],
        ["Substituted Words", str(result.substituted_words)],
        ["Inserted Words",    str(result.inserted_words)],
    ]
    t = Table(summary_data, colWidths=[8*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.6*cm))

    # Word-by-word table
    elements.append(Paragraph("<b>Word-by-Word Analysis</b>", styles["Heading2"]))
    elements.append(Spacer(1, 0.2*cm))
    word_header = ["#", "Expected", "Spoken", "Status", "Score"]
    word_rows   = [word_header]
    for a in result.alignments:
        word_rows.append([
            str(a.index + 1),
            a.expected,
            a.spoken if a.spoken else "—",
            a.status.capitalize(),
            f"{a.similarity:.0f}",
        ])
    wt = Table(word_rows, colWidths=[1*cm, 4*cm, 4*cm, 3*cm, 2*cm])
    wt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0f9ff")]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(wt)

    doc.build(elements)
    return buf.getvalue()


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
        try:
            pdf_bytes = _build_pdf(result)
            st.download_button(
                "📑 Download PDF",
                data=pdf_bytes,
                file_name=f"result_{result.article_id}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.warning(f"PDF generation failed: {e}")

    with col_back:
        if st.button("⬅ Back to Reading", use_container_width=True):
            st.session_state.show_dashboard = False
            st.rerun()
