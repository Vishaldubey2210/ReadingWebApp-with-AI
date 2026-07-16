"""
==========================================================
ReadingAI - Home Page
Real-Time Reading Coach
Author : Vishal Kumar
==========================================================
"""

import streamlit as st

from config import APP_NAME, APP_VERSION
from services.article_service import get_article_service


# ==========================================================
# HEADER
# ==========================================================

def show_header():
    st.title("📖 ReadingAI")
    st.caption(f"{APP_NAME} | Version {APP_VERSION}")
    st.divider()


# ==========================================================
# SETTINGS — Language / Difficulty / Category
# ==========================================================

def settings(service):
    st.subheader("⚙️ Settings")

    available_difficulties = service.get_difficulties()
    available_languages    = service.get_languages()

    if not available_languages:
        st.error("No articles found. Please add articles to the `articles/` directory.")
        return

    col_lang, col_diff, col_cat = st.columns(3)
    with col_lang:
        language = st.selectbox(
            "Language", available_languages, index=0,
            help="Select the reading language"
        )
    with col_diff:
        difficulty = st.selectbox(
            "Difficulty", available_difficulties, index=0,
            help="Select the difficulty level"
        )

    available_categories = service.get_categories(language=language, difficulty=difficulty)
    with col_cat:
        category = st.selectbox(
            "Category", available_categories if available_categories else ["—"],
            index=0, help="Filter by category"
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Random Article", use_container_width=True, type="primary"):
            article = service.get_random_article(
                difficulty=difficulty,
                language=language,
                category=category
            )
            if article:
                st.session_state.article           = article
                st.session_state.article_text      = article.content
                st.session_state.difficulty        = difficulty
                st.session_state.language          = language
                st.session_state.reading_completed = False
                st.session_state.result            = None
                st.session_state.show_dashboard    = False
                st.toast(f"Loaded: {article.title}", icon="📖")
            else:
                st.error("No articles found matching the selected settings.")
            st.rerun()

    with col2:
        if st.button("🗑 Clear", use_container_width=True):
            for k in ("article", "article_text", "result"):
                st.session_state[k] = None
            st.session_state.article_text      = ""
            st.session_state.reading_completed = False
            st.session_state.show_dashboard    = False
            st.rerun()


# ==========================================================
# ARTICLE METADATA VIEW
# ==========================================================

def article_view():
    st.subheader("📄 Article")

    article = st.session_state.get("article")
    if not article or not st.session_state.get("article_text", ""):
        st.info("Select options above and click **Random Article** to load text.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Title", article.title)
    with col2:
        st.metric("Est. Reading Time", f"{article.estimated_reading_time_minutes} min")
    with col3:
        st.metric("Word Count", f"{article.word_count} words")

    tags_str = ", ".join(article.tags)
    st.markdown(
        f"**Category:** `{article.category}` | **Difficulty:** `{article.difficulty}` | "
        f"**Author:** `{article.author}` | **Source:** `{article.source.upper()}`"
    )
    if tags_str:
        st.markdown(f"**Tags:** {tags_str}")

    with st.expander("👁 Preview Article Text", expanded=False):
        st.write(st.session_state.article_text)


# ==========================================================
# REAL-TIME READING SECTION
# ==========================================================

def realtime_reading_section():
    import json
    from core.scoring import ReadingResult, WordAlignmentResult
    from ui.realtime_reader import realtime_reader

    st.subheader("🎙️ Real-Time Reading Coach")

    article = st.session_state.get("article")
    if not article:
        st.info("💡 Load an article first to start the reading coach.")
        return

    # ── Legend ────────────────────────────────────────────────
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            "<div style='background:#1e293b;border-radius:10px;padding:10px 14px;"
            "border-left:3px solid #fbbf24;font-size:0.85rem'>"
            "<b>🟡 Yellow</b> — Current word<br>Read this word aloud</div>",
            unsafe_allow_html=True
        )
    with col_b:
        st.markdown(
            "<div style='background:#1e293b;border-radius:10px;padding:10px 14px;"
            "border-left:3px solid #4ade80;font-size:0.85rem'>"
            "<b>🟢 Green</b> — Correct!<br>Word matched perfectly</div>",
            unsafe_allow_html=True
        )
    with col_c:
        st.markdown(
            "<div style='background:#1e293b;border-radius:10px;padding:10px 14px;"
            "border-left:3px solid #f87171;font-size:0.85rem'>"
            "<b>🔴 Red</b> — Wrong word<br>Retry or click Skip ⏭</div>",
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Render the embedded real-time coach (no return value) ──
    article_words = st.session_state.article_text.split()
    realtime_reader(article_words=article_words)

    # ── Result submission form below the component ─────────────
    st.markdown("---")
    st.caption("📋 When done reading, paste the result JSON here and click Submit:")

    with st.form("reading_result_form", clear_on_submit=True):
        raw_json = st.text_area(
            "Result JSON (auto-filled by coach)",
            height=80,
            placeholder='{"finished": true, "accuracy": 85, ...}',
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("✅ Submit Reading Results", use_container_width=True)

    if submitted and raw_json.strip():
        try:
            result = json.loads(raw_json.strip())
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON. Please copy the result from the coach.")
            return

        if not result.get("finished"):
            st.warning("Incomplete session — finish reading first.")
            return

        word_results = sorted(result.get("word_results", []), key=lambda r: r.get("index", 0))

        alignments = []
        for r in word_results:
            if not r.get("expected"):
                continue
            status = r["status"]
            if status == "wrong":
                status = "substituted"
            alignments.append(
                WordAlignmentResult(
                    index=r["index"],
                    expected=r["expected"],
                    spoken=r.get("spoken", ""),
                    status=status,
                    similarity=float(r.get("similarity", 0))
                )
            )

        reading_result = ReadingResult(
            accuracy=float(result.get("accuracy", 0)),
            wpm=float(result.get("wpm", 0)),
            reading_time_sec=float(result.get("reading_time_sec", 0)),
            total_words=int(result.get("total_words", len(article_words))),
            correct_words=int(result.get("correct_words", 0)),
            skipped_words=int(result.get("skipped_words", 0)),
            substituted_words=int(result.get("error_words", 0)),
            inserted_words=0,
            article_title=article.title,
            article_id=article.id,
            alignments=alignments,
            inserted_word_list=[],
            transcript="",
            audio_path=""
        )

        st.session_state.result = reading_result
        st.session_state.reading_completed = True

        # Save to DB (non-blocking)
        try:
            from database.database import Database
            db = Database()
            db.insert_result(
                student_name="Guest Student",
                article_name=article.title,
                accuracy=reading_result.accuracy,
                fluency=reading_result.accuracy,
                pronunciation=reading_result.accuracy,
                wpm=reading_result.wpm,
                score=reading_result.accuracy,
                total_words=reading_result.total_words,
                correct_words=reading_result.correct_words,
                wrong_words=reading_result.substituted_words + reading_result.skipped_words,
                attempts=1
            )
        except Exception:
            pass

        st.success("✅ Reading session saved!")
        if st.button("📊 View Full Dashboard", use_container_width=True, type="primary"):
            st.session_state.show_dashboard = True
            st.rerun()


# ==========================================================
# MAIN HOME
# ==========================================================

def show_home():
    article_service = get_article_service()

    # Sidebar diagnostics
    validation_logs = article_service.get_validation_logs()
    if validation_logs:
        with st.sidebar.expander("⚠️ Article Scanning Diagnostics", expanded=False):
            st.caption("Issues detected during articles folder scan:")
            for log in validation_logs:
                st.warning(log)

    show_header()
    settings(article_service)
    st.divider()
    article_view()
    st.divider()
    realtime_reading_section()