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
    st.selectbox(
        "Language / Sprache",
        options=["Deutsch", "English"],
        key="language_selection",
        label_visibility="collapsed",
        width="stretch",
        on_change=_switch_language,
        args=(german_page, english_page),
    )
