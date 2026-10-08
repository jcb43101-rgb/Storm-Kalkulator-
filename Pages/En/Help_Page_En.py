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
        "The most important specs to include are: power in watts, voltage, and power factor. "
        "Use 230 V for single-phase equipment and 400 V for three-phase equipment. "
        "You also need to include how many of each device you are going to be using, and if on a larger set, " 
        "which department the device belongs to, i.e. Production, audio, video, catering, or lighting. " 
        "You can create this list on our online calculator but it does not automatically save, so be careful," 
        "refreshing the page will cause the data to be reset! You can also create a csv file with the device list " 
        "data and upload it to be automatically filled into our calculator.\n\n""As you are filling in the device list " 
        "on the calculator page, our mathematical algorithm automatically updates the calculations at the bottom "
        "of the page to take all the devices into account. You can then sort by different views of the data, " 
        "including specs per device or by department.\n\n" "If you are using 3phase power or generators there is also " 
        "a tab to recommend a way to divide the devices among the three phases to ensure that power is distributed " 
"equally. As a planning target, aim to keep the phases within 10% of one "
"another in kVA, then verify the final distribution with your power "
"technician. \n\n" "The last tab is where you can export a pdf "
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

    st.subheader("How the calculator estimates your set's power")
    st.write(
        "Think of each equipment row as one part of your production's power "
        "plan: a row might be a group of LED fixtures, a camera package, a "
        "sound system, or catering equipment. The calculator multiplies the "
        "quantity by the power of one item to find that row's total watts (W). "
        "It adds all row totals and divides by 1,000 to show the set's active "
        "power in kilowatts (kW).\n\n"
        "For each row, the calculator estimates current as: total row watts / "
        "(voltage x power factor). Apparent power is calculated as: total row "
        "watts / power factor. The row's apparent power is converted to "
        "kilovolt-amperes (kVA), then added to the other rows. The power factor "
        "(PF, or cos phi) accounts for the difference between active power "
        "(kW), which does useful work, and apparent power (kVA), which helps "
        "size a generator and electrical supply.\n\n"
        "This current formula is a single-phase estimate. For a 400 V "
        "three-phase device, use the manufacturer's rated current or have a "
        "qualified power technician verify the line current; the calculator's "
        "row-current estimate does not include a three-phase adjustment.\n\n"
        "For example, four 420 W LED fixtures have a combined active load of "
        "1,680 W, or 1.68 kW. At 230 V with a power factor of 0.99, their "
        "estimated current is 1,680 / (230 x 0.99), or about 7.38 A. Their "
        "apparent load is about 1.70 kVA.\n\n"
        "The overview's total current at 230 V is a simplified comparison: "
        "total watts / 230. It is not the sum of the actual currents of "
        "equipment using different voltages. For the generator estimate, the "
        "calculator adds a 25% planning margin to the total kVA and suggests "
        "the next listed standard generator size at or above that amount, "
        "when one is available.\n\n"
        "In the phase-balancing view, each 400 V three-phase row is split "
        "equally across L1, L2, and L3. The 230 V single-phase rows are sorted "
        "from largest to smallest and assigned one at a time to the phase with "
        "the least active power so far. This is a planning estimate based on "
        "watts; it does not account for start-up surges, changing loads, cable "
        "or breaker limits, or every real-world power-factor effect. Confirm "
        "the equipment specifications and final distribution with a qualified "
        "electrician or power technician before the shoot."
    )
