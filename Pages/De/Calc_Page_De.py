import pandas as pd
import streamlit as st
from Pages.De.Help_Page_De import Help_Page_View_De 
from Utilities.Master_Calc import render_calculations


def Calc_Page_View_De(Help_Page_View_De):
    # Top header with right-aligned button
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.title("⚡ Filmset Strom- & Lastenrechner")
    with col_btn:
        st.write("")  # Vertical spacing adjustment
        if st.button("❓ Hilfe / Info", use_container_width=True):
            st.switch_page(Help_Page_View_De)

    st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
                        "ersetzt keine professionelle Elektroplanung. "
                        "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")

    st.write(
        "Füge deine Set-Geräte unten ein, um Ein- und Drehstromlasten zu berechnen, "
        "Abteilungsanalysen einzusehen, Phasen (L1, L2, L3) automatisch abzugleichen und passende PDF-Berichte zu erstellen."
    )

    # --- Projekt-Informationen ---
    col_proj, col_director, col_gaffer = st.columns(3)
    with col_proj:
        project_name = st.text_input("Projektname", "Studentischer Kurzfilm")
    with col_director:
        director = st.text_input("Regie / Kurs", "Medienproduktion 101")
    with col_gaffer:
        gaffer = st.text_input("Oberbeleuchter / Gaffer", "Name des Studenten")

    st.divider()

    # --- Abteilungen ---
    DEPARTMENTS = ["Licht", "Ton", "Kamera / Video", "Produktion", "Catering"]

    # --- Interaktiver Dateneditor ---
    st.subheader("Geräteliste")
    st.info("Es ist sehr wichtig, dass des Wert der Leistungs ist auf Watt (W) " 
    "und nicht auf Kilowatt (kW) eingestellt ist. " 
    "Um Watt in Kilowatt umzurechnen, teile die Wattzahl durch 1000. Beispiel: 1500 W = 1,5 kW.")
    default_data = pd.DataFrame(
        [
            {
                "Gerätename": "Beispielleuchte ",
                "Abteilung": "Licht",
                "Anzahl": 4,
                "Leistung_W": 420,
                "Power_Factor": 0.99,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Beispiel-Lautsprecher",
                "Abteilung": "Ton",
                "Anzahl": 1,
                "Leistung_W": 250,
                "Power_Factor": 0.95,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Beispielkamera",
                "Abteilung": "Kamera / Video",
                "Anzahl": 1,
                "Leistung_W": 850,
                "Power_Factor": 0.96,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Beispiel Catering-Ausstattung",
                "Abteilung": "Catering",
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.00,
                "Spannung_V": 230,
            },
            {
                "Gerätename": "Beispiel Production-Ausstattung",
                "Abteilung": "Produktion",
                "Anzahl": 1,
                "Leistung_W": 2800,
                "Power_Factor": 1.00,
                "Spannung_V": 230,
            },
        ]
    )

    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config={
            "Gerätename": st.column_config.TextColumn("Gerätename", required=True, width="medium"),
            "Abteilung": st.column_config.SelectboxColumn("Abteilung", options=DEPARTMENTS, default="Licht", required=True),
            "Anzahl": st.column_config.NumberColumn("Anzahl", min_value=1, step=1, default=1),
            "Leistung_W": st.column_config.NumberColumn("Leistung (Watt)", min_value=1, step=10, default=100),
            "Power_Factor": st.column_config.NumberColumn("Leistungsfaktor / Cos φ (0.1 - 1.0)", min_value=0.1, max_value=1.0, step=0.01, default=0.95),
            "Spannung_V": st.column_config.SelectboxColumn("Spannung (V)", options=[230, 400], default=230),
        },
        use_container_width=True,
    )
    render_calculations(
        edited_df,
        project_name=project_name,
        director=director,
        gaffer=gaffer,
        language="de",
    )
