import pandas as pd
import streamlit as st

from Utilities.Master_Calc import render_calculations
from Utilities.Language_Selection import apply_header_styles, language_selection
from Utilities.Equipment_CSV_Import import (
    CSV_IMPORT_TEXT,
    render_equipment_csv_import,
)


def Calc_Page_View_En(help_page_en, calc_page_de, calc_page_en, language_pages=None):
    apply_header_styles()
    col_title, col_controls = st.columns(
        [0.56, 0.44], vertical_alignment="bottom", wrap=False
    )
    with col_title:
        st.title("⚡ Film Set Power & Load Calculator")
    with col_controls:
        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="bottom",
            gap="small",
            key="header_controls",
        ):
            language_selection(
                calc_page_de,
                calc_page_en,
                "English",
                additional_pages=language_pages,
            )
            if st.button(
                "Help/Information",
                width="content",
                key="header_navigation_button",
            ):
                st.switch_page(help_page_en)

    st.info(
        "**Important:** This calculator is a planning aid and does not replace "
        "professional electrical planning. Please carefully verify all "
        "calculations and recommendations."
    )

    st.write(
        "Enter your production equipment below to calculate single- and "
        "three-phase loads, review department breakdowns, automatically balance "
        "phases (L1, L2, L3), and create PDF reports."
    )

    col_proj, col_director, col_gaffer = st.columns(3)
    with col_proj:
        project_name = st.text_input("Project Name", "Student Short Film")
    with col_director:
        director = st.text_input("Director / Course", "Media Production 101")
    with col_gaffer:
        gaffer = st.text_input("Gaffer / Chief Lighting Technician", "Student Name")

    st.divider()

    departments = ["Lighting", "Sound", "Camera / Video", "Production", "Catering"]

    st.subheader("Equipment List")
    st.info(
        "Make sure power is entered in watts (W), not kilowatts (kW). "
        "To convert watts to kilowatts, divide by 1,000. For example: "
        "1,500 W = 1.5 kW."
    )
    default_data = pd.DataFrame(
        [
            {
                "Gerätename": "Sample light",
                "Abteilung": "Lighting",
                "Anzahl": 4,
                "Leistung_W": 420,
                "Power_Factor": 0.99,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Sample speaker",
                "Abteilung": "Sound",
                "Anzahl": 1,
                "Leistung_W": 250,
                "Power_Factor": 0.95,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Sample camera",
                "Abteilung": "Camera / Video",
                "Anzahl": 1,
                "Leistung_W": 850,
                "Power_Factor": 0.96,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Sample catering equipment",
                "Abteilung": "Catering",
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.00,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Sample production equipment",
                "Abteilung": "Production",
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.00,
                "Spannung_V": 230,
            },
        ]
    )

    csv_text = CSV_IMPORT_TEXT["en"]
    edited_df = render_equipment_csv_import(
        default_data,
        locale="en",
        departments=departments,
        upload_label=csv_text["label"],
        help_text=csv_text["help"],
        success_text=csv_text["success"],
        editor_key="equipment_editor_en",
        column_config={
            "Gerätename": st.column_config.TextColumn("Equipment Name", required=True, width="medium"),
            "Abteilung": st.column_config.SelectboxColumn(
                "Department", options=departments, default="Lighting", required=True
            ),
            "Anzahl": st.column_config.NumberColumn("Quantity", min_value=1, step=1, default=1),
            "Leistung_W": st.column_config.NumberColumn("Power (W)", min_value=1, step=10, default=100),
            "Power_Factor": st.column_config.NumberColumn(
                "Power Factor / Cos φ (0.1–1.0)",
                min_value=0.1,
                max_value=1.0,
                step=0.01,
                default=0.95,
            ),
            "Spannung_V": st.column_config.SelectboxColumn(
                "Voltage (V)", options=[230, 400], default=230
            ),
        },
    )
    render_calculations(
        edited_df,
        project_name=project_name,
        director=director,
        gaffer=gaffer,
        language="en",
    )
