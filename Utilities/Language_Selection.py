import streamlit as st

from Utilities.Translations import LOCALE_NAMES


def _switch_language(pages: dict[str, st.Page]):
    selected_language = st.session_state["language_selection"]
    if selected_language not in pages:
        raise ValueError(f"Unsupported language selection: {selected_language}")
    st.switch_page(pages[selected_language])


def apply_header_styles():
    st.markdown(
        """
        <style>
        .stHorizontalBlock:has(> [data-testid="stColumn"] h1)
        > [data-testid="stColumn"]:first-child {
            container-type: inline-size;
        }
        .stHorizontalBlock:has(> [data-testid="stColumn"] h1) {
            overflow: visible !important;
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
        .st-key-language_selection {
            flex: 0 1 max-content !important;
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
            .st-key-header_controls {
                width: calc(100% + 8px) !important;
                margin-left: -8px;
                gap: 4px !important;
            }
        }
        @media (max-width: 380px) {
            .st-key-header_controls {
                width: 100% !important;
                margin-left: 0;
                flex-direction: column !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def language_selection(
    german_page,
    english_page,
    current_language,
    *,
    additional_pages: dict[str, st.Page] | None = None,
):
    pages = {
        LOCALE_NAMES["de"]: german_page,
        LOCALE_NAMES["en"]: english_page,
        **(additional_pages or {}),
    }
    language_options = {name: name for name in pages}
    selected_current_language = {
        "Deutsch": LOCALE_NAMES["de"],
        "English": LOCALE_NAMES["en"],
    }.get(current_language, current_language)
    placeholder = (
        "Sprache wählen 🇩🇪"
        if selected_current_language.startswith(("Deutsch",))
        else "Select language 🇬🇧"
    )
    st.session_state["language_selection"] = None
    st.selectbox(
        "Language / Sprache",
        options=list(language_options),
        key="language_selection",
        index=None,
        placeholder=placeholder,
        label_visibility="collapsed",
        format_func=language_options.__getitem__,
        width="stretch",
        on_change=_switch_language,
        args=(pages,),
    )
