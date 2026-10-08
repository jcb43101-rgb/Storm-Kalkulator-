from pathlib import Path

import pandas as pd
import streamlit as st

from Utilities.Language_Selection import apply_header_styles, language_selection
from Utilities.Master_Calc import render_calculations
from Utilities.Translations import LOCALE_NAMES, PAGE_TEXT, Locale


def _text(locale: Locale, key: str) -> str:
    value = PAGE_TEXT[locale][key]
    if not isinstance(value, str):
        raise TypeError(f"Expected localized text for {locale}.{key}")
    return value


def _text_list(locale: Locale, key: str) -> list[str]:
    value = PAGE_TEXT[locale][key]
    if not isinstance(value, list):
        raise TypeError(f"Expected localized list for {locale}.{key}")
    return value


def render_localized_calculator(
    locale: Locale,
    calculator_pages: dict[str, st.Page],
    help_pages: dict[str, st.Page],
) -> None:
    text = lambda key: _text(locale, key)
    apply_header_styles(locale)
    title_column, controls_column = st.columns(
        [0.56, 0.44], vertical_alignment="bottom", wrap=False
    )
    with title_column:
        st.title(text("calc_title"))
    with controls_column:
        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="bottom",
            gap="small",
            key="header_controls",
        ):
            language_selection(
                calculator_pages[LOCALE_NAMES[locale]],
                calculator_pages["English 🇬🇧"],
                LOCALE_NAMES[locale],
                additional_pages=calculator_pages,
            )
            if st.button(
                text("help_button"),
                width="content",
                key="header_navigation_button",
            ):
                st.switch_page(help_pages[LOCALE_NAMES[locale]])

    st.info(text("important"))
    st.write(text("intro"))

    project_column, director_column, gaffer_column = st.columns(3)
    with project_column:
        project_name = st.text_input(text("project"), text("default_project"))
    with director_column:
        director = st.text_input(text("director"), text("default_director"))
    with gaffer_column:
        gaffer = st.text_input(text("gaffer"), text("default_gaffer"))

    st.divider()
    st.subheader(text("equipment_list"))
    st.info(text("watt_info"))

    departments = _text_list(locale, "departments")
    equipment_names = _text_list(locale, "sample_equipment")
    default_data = pd.DataFrame(
        [
            {
                "Gerätename": equipment_names[0],
                "Abteilung": departments[0],
                "Anzahl": 4,
                "Leistung_W": 420,
                "Power_Factor": 0.99,
                "Spannung_V": 230,
            },
            {
                "Gerätename": equipment_names[1],
                "Abteilung": departments[1],
                "Anzahl": 1,
                "Leistung_W": 250,
                "Power_Factor": 0.95,
                "Spannung_V": 230,
            },
            {
                "Gerätename": equipment_names[2],
                "Abteilung": departments[2],
                "Anzahl": 1,
                "Leistung_W": 850,
                "Power_Factor": 0.96,
                "Spannung_V": 230,
            },
            {
                "Gerätename": equipment_names[3],
                "Abteilung": departments[4],
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.0,
                "Spannung_V": 230,
            },
            {
                "Gerätename": equipment_names[4],
                "Abteilung": departments[3],
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.0,
                "Spannung_V": 230,
            },
        ]
    )
    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Gerätename": st.column_config.TextColumn(
                text("equipment_name"), required=True, width="medium"
            ),
            "Abteilung": st.column_config.SelectboxColumn(
                text("department"),
                options=departments,
                default=departments[0],
                required=True,
            ),
            "Anzahl": st.column_config.NumberColumn(
                text("quantity"), min_value=1, step=1, default=1
            ),
            "Leistung_W": st.column_config.NumberColumn(
                text("power"), min_value=1, step=10, default=100
            ),
            "Power_Factor": st.column_config.NumberColumn(
                text("power_factor"),
                min_value=0.1,
                max_value=1.0,
                step=0.01,
                default=0.95,
            ),
            "Spannung_V": st.column_config.SelectboxColumn(
                text("voltage"), options=[230, 400], default=230
            ),
        },
        use_container_width=True,
    )
    render_calculations(
        edited_df,
        project_name=project_name,
        director=director,
        gaffer=gaffer,
        language=locale,
    )


def render_localized_help(
    locale: Locale,
    calculator_pages: dict[str, st.Page],
    help_pages: dict[str, st.Page],
) -> None:
    text = lambda key: _text(locale, key)
    apply_header_styles(locale)
    title_column, controls_column = st.columns(
        [0.56, 0.44], vertical_alignment="bottom", wrap=False
    )
    with title_column:
        st.title(text("help_title"))
    with controls_column:
        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="bottom",
            gap="small",
            key="header_controls",
        ):
            language_selection(
                help_pages[LOCALE_NAMES[locale]],
                help_pages["English 🇬🇧"],
                LOCALE_NAMES[locale],
                additional_pages=help_pages,
            )
            if st.button(
                text("calc_button"),
                width="content",
                key="header_navigation_button",
            ):
                st.switch_page(calculator_pages[LOCALE_NAMES[locale]])

    st.info(text("important"))
    st.divider()
    st.markdown(
        """
        <style>
        .st-key-tutorial_titles :is(h1, h2, h3, h4, h5, h6) {
            white-space: nowrap;
            font-size: 1.7rem;
        }
        .st-key-tutorial_titles [data-testid="stColumn"]:last-child h1 {
            text-align: right;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.container(key="tutorial_titles"):
        text_title, video_title = st.columns([2.5, 1])
        with text_title:
            st.title(text("help_text_title"))
        with video_title:
            st.title(text("video_title"))

    tutorial_text, tutorial_video = st.columns([2.5, 1], wrap=False)
    with tutorial_text:
        st.write(
            "\n\n".join(
                text(key)
                for key in (
                    "help_intro",
                    "help_workflow",
                    "help_analysis",
                    "help_phase",
                    "help_reports",
                    "help_limits",
                )
            )
        )
    with tutorial_video:
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width="stretch")
        for image_name in (
            "400VAmps.png",
            "230VAmps.png",
            "kW.pF.kVA.png",
            "kWx1000.W.png",
        ):
            st.image(
                Path(__file__).resolve().parents[1] / "photos" / image_name,
                width="stretch",
            )

    st.subheader(text("math_title"))
    st.write(text("math"))
