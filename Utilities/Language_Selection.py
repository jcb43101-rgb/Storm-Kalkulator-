import streamlit as st


def _switch_language(german_page, english_page):
    selected_language = st.session_state["language_selection"]
    pages = {
        "Deutsch": german_page,
        "English": english_page,
    }
    st.switch_page(pages[selected_language])


def apply_header_styles():
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
        .st-key-language_selection,
        .st-key-language_selection [data-testid="stSelectbox"] {
            width: max-content !important;
            max-width: 100%;
        }
        .st-key-language_selection [data-baseweb="select"] {
            width: max-content !important;
            max-width: 100%;
        }
        .st-key-language_selection [data-testid="stSelectbox"] input {
            caret-color: transparent !important;
        }
        .st-key-header_controls {
            gap: 0.5rem !important;
            position: relative;
            left: 0.625rem;
        }
        .st-key-header_navigation_button {
            width: fit-content !important;
        }
        .st-key-header_navigation_button [data-testid="stBaseButton-secondary"] {
            width: fit-content !important;
            flex: 0 0 auto;
        }
        @media (max-width: 950px) {
            .stHorizontalBlock:has(> [data-testid="stColumn"] h1) {
                flex-wrap: wrap !important;
            }
            .stHorizontalBlock:has(> [data-testid="stColumn"] h1)
            > [data-testid="stColumn"] {
                flex: 1 1 100% !important;
                width: 100% !important;
                min-width: 0 !important;
            }
            .st-key-language_selection {
                flex: 0 0 156px !important;
                max-width: 156px;
            }
            .st-key-header_controls {
                left: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def language_selection(german_page, english_page, current_language):
    st.session_state["language_selection"] = None
    language_options = {
        "Deutsch": "Deutsch 🇩🇪",
        "English": "English 🇬🇧",
    }
    placeholder = (
        "Sprache wählen 🇩🇪"
        if current_language == "Deutsch"
        else "Select language 🇬🇧"
    )
    st.selectbox(
        "Language / Sprache",
        options=["Deutsch", "English"],
        key="language_selection",
        index=None,
        placeholder=placeholder,
        label_visibility="collapsed",
        format_func=language_options.__getitem__,
        width="stretch",
        on_change=_switch_language,
        args=(german_page, english_page),
    )
