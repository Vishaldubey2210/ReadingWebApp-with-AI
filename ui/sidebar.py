import streamlit as st

from config import APP_NAME, APP_VERSION


def show_sidebar():

    with st.sidebar:

        st.title("📖 ReadingAI")

        st.caption(f"Version {APP_VERSION}")

        st.divider()

        st.markdown("### 👤 Student")

        st.metric(
            label="Accuracy",
            value=f"{st.session_state.accuracy}%"
        )

        st.metric(
            label="Reading Speed",
            value=f"{st.session_state.wpm} WPM"
        )

        st.metric(
            label="Fluency",
            value=f"{st.session_state.fluency}%"
        )

        st.divider()

        st.markdown("### 📄 Current Session")

        st.write(
            f"**Difficulty:** {st.session_state.difficulty}"
        )

        st.write(
            f"**Language:** {st.session_state.language}"
        )

        if st.session_state.article is not None:

            st.success(
                f"Loaded : {st.session_state.article.name}"
            )

        else:

            st.warning("No Article Loaded")

        st.divider()

        st.markdown("### 🎯 Progress")

        total_words = len(
            st.session_state.article_text.split()
        )

        current_word = st.session_state.current_word_index

        progress = 0

        if total_words != 0:

            progress = current_word / total_words

        st.progress(progress)

        st.write(
            f"{current_word} / {total_words} Words"
        )

        st.divider()

        st.markdown("### ⚙️ Status")

        if st.session_state.reading_started:

            st.success("Reading Started")

        else:

            st.info("Waiting")

        if st.session_state.reading_completed:

            st.success("Completed")

        st.divider()

        st.caption(APP_NAME)