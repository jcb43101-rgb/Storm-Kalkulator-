from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import language_selection


def Help_Page_View_En(calc_page_en, help_page_de, help_page_en):
    col_title, col_btn, col_language = st.columns(
        [0.68, 0.16, 0.16], vertical_alignment="bottom"
    )
    with col_title:
        st.title("❓ Help & Documentation")
    with col_btn:
        if st.button("⬅️ Back to Calculator", use_container_width=True):
            st.switch_page(calc_page_en)
    with col_language:
        language_selection(help_page_de, help_page_en, "English")

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
