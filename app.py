"""
==========================================================
ReadingAI
Main Entry Point

Author : Vishal Kumar
==========================================================
"""

import sys
import os

# ==========================================================
# TYPING COMPATIBILITY PATCH
# Fixes Python 3.11 typing.Generic / typing.Concatenate
# compatibility with typing_extensions.ParamSpec on Windows
# ==========================================================
try:
    import typing
    import typing_extensions

    # Patch typing._is_typevar_like
    _orig_is_typevar_like = typing._is_typevar_like
    def _patched_is_typevar_like(x):
        return _orig_is_typevar_like(x) or isinstance(x, typing_extensions.ParamSpec)
    typing._is_typevar_like = _patched_is_typevar_like

    # Patch typing.Concatenate
    _orig_concatenate_getitem = typing.Concatenate._getitem
    def _patched_concatenate_getitem(self, parameters):
        if not isinstance(parameters, tuple):
            parameters = (parameters,)
        last_param = parameters[-1]
        if isinstance(last_param, typing_extensions.ParamSpec):
            dummy = typing.ParamSpec(last_param.__name__)
            temp_params = parameters[:-1] + (dummy,)
            res = _orig_concatenate_getitem(self, temp_params)
            res.__args__ = res.__args__[:-1] + (last_param,)
            return res
        return _orig_concatenate_getitem(self, parameters)
    typing.Concatenate._getitem = _patched_concatenate_getitem
except Exception:
    pass


# ==========================================================
# PAGE CONFIG — must be the very first Streamlit call
# ==========================================================
import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, LAYOUT

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
)

# ==========================================================
# APP IMPORTS
# ==========================================================
from ui.home import show_home          # noqa: E402
from ui.Dashboard import show_dashboard  # noqa: E402

# ==========================================================
# SESSION STATE
# ==========================================================
DEFAULT_SESSION = {
    "article": None,
    "article_text": "",
    "difficulty": "Easy",
    "language": "English",
    "reading_started": False,
    "reading_completed": False,
    "current_word_index": 0,
    "spoken_text": "",
    "accuracy": 0.0,
    "fluency": 0.0,
    "wpm": 0.0,
    "score": 0.0,
    "errors": [],
    "attempts": {},
    # Audio pipeline
    "recorded_audio_path": None,
    "transcript": "",
    "last_processed_audio": None,
    "duration_seconds": 0.0,
    # Analysis results
    "alignment": [],
    "result": None,
    "show_dashboard": False,
}

for key, value in DEFAULT_SESSION.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================================
# MAIN APP
# ==========================================================
def main():
    if st.session_state.get("show_dashboard"):
        show_dashboard()
    else:
        show_home()


# ==========================================================
# START
# ==========================================================
if __name__ == "__main__":
    main()