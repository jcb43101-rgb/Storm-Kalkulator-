import streamlit as st


def _switch_language(german_page, english_page):
    selected_language = st.session_state["language_selection"]
    pages = {
        "Deutsch": german_page,
        "English": english_page,
    }
    st.switch_page(pages[selected_language])


def language_selection(german_page, english_page, current_language):
    st.session_state["language_selection"] = current_language
    language_options = {
        "Deutsch": "🇩🇪 Deutsch",
        "English": "🇬🇧 English",
    }
    st.markdown(
        """
        <style>
        .stHorizontalBlock:has(> [data-testid="stColumn"] h1)
        > [data-testid="stColumn"]:first-child {
            container-type: inline-size;
        }
        .stHorizontalBlock:has(> [data-testid="stColumn"] h1)
        > [data-testid="stColumn"]:first-child h1 {
            white-space: nowrap;
            font-size: clamp(0.625rem, 5cqw, 2.5rem);
        }
        .st-key-language_selection [data-testid="stSelectbox"] *,
        .st-key-language_selection [data-testid="stSelectbox"] input {
            cursor: default !important;
        }
        .st-key-language_selection [data-testid="stSelectbox"] input {
            caret-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    label = (
        "🇩🇪 Sprache wählen"
        if current_language == "Deutsch"
        else "🇬🇧 Select language"
    )
    st.selectbox(
        label,
        options=["Deutsch", "English"],
        key="language_selection",
        format_func=language_options.__getitem__,
        width="stretch",
        on_change=_switch_language,
        args=(german_page, english_page),
    )
