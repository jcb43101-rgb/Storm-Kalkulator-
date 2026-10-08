from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import apply_header_styles, language_selection


def Help_Page_View_En(calc_page_en, help_page_de, help_page_en):
    apply_header_styles()
    col_title, col_controls = st.columns(
        [0.56, 0.44], vertical_alignment="bottom", wrap=False
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
        tutorial_text_title, tutorial_video_title = st.columns([2.5, 1])
        with tutorial_text_title:
            st.title("Instructions & Information")
        with tutorial_video_title:
            st.title("Video Tutorial in English")

    tutorial_text, tutorial_video = st.columns([2.5, 1], wrap=False)
        
    with tutorial_text:
        st.write("In order to calculate the Load you will need to supply all your devices on your film set, " 
        "the first thing you need to do is create an inventory list of every device and its technical specs. " 
        "The most important specs to include are: Wattage, Amps, if it is 1 or 3 phasic and if its AC or DC. " 
        "You also need to include how many of each device you are going to be using, and if on a larger set, " 
        "which department the device belongs to, i.e. Production, audio, video, catering, or lighting. " 
        "You can create this list on our online calculator but it does not automatically save, so be careful," 
        "refreshing the page will cause the data to be reset! You can also create a csv file with the device list " 
        "data and upload it to be automatically filled into our calculator.\n\n""As you are filling in the device list " 
        "on the calculator page, our mathematical algorithm automatically updates the calculations at the bottom "
        "of the page to take all the devices into account. You can then sort by different views of the data, " 
        "including specs per device or by department.\n\n" "If you are using 3phase power or generators there is also " 
        "a tab to recommend a way to divide the devices among the three phases to ensure that power is distributed " 
"equally. Each phase should be within 10% kVA of one another. \n\n" "The last tab is where you can export a pdf "
        "of the data from your device list, there are four different structures and you can choose which one or "
        "(four) fit your needs best. You can then print and distribute the pdfs to your team!\n\n" "The specific math "
        "formulations we use in our algorithm will be shared below. \n\n" "Break a Leg! ")
        st.info("Learn about the math and formulas used in the online calculator.")
    
    with tutorial_video:
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)
        st.image(Path(__file__).resolve().parents[2] / "photos" / "400VAmps.png", width=500)
        st.image(Path(__file__).resolve().parents[2] / "photos" / "230VAmps.png", width=500)
        st.image(Path(__file__).resolve().parents[2] / "photos" / "kW.pF.kVA.png", width=500)
        st.image(Path(__file__).resolve().parents[2] / "photos" / "kWx1000.W.png", width=500)
