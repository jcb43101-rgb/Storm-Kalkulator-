from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import apply_header_styles, language_selection


def Help_Page_View_En(calc_page_en, help_page_de, help_page_en):
    apply_header_styles()
    col_title, col_controls = st.columns(
        [0.62, 0.38], vertical_alignment="bottom", wrap=False
    )
    with col_title:
        st.title("❓ Help & Documentation")
    with col_controls:
        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="bottom",
            gap="small",
            key="header_controls",
        ):
            language_selection(help_page_de, help_page_en, "English")
            if st.button(
                "Calculator",
                width="content",
                key="header_navigation_button",
            ):
                st.switch_page(calc_page_en)

    st.info(
        "**Important:** This calculator is a planning aid and does not replace "
        "professional electrical planning. Please carefully verify all "
        "calculations and recommendations."
    )

    st.divider()

    st.title("Instructions & Information")

    st.header("Video Tutorial in English")

    st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)

    st.info("Learn about the math and formulas used in the online calculator.")
    
    st.image(Path(__file__).resolve().parents[2] / "photos" / "400VAmps.png")
