import math
from pathlib import Path
import pandas as pd
import streamlit as st
from Utilities.pdf_helpers_De import generate_pdf_report_De
from Utilities.pdf_helpers_En import generate_pdf_report_En
from Utilities.calculator_de import main_calculator_de
from app import calc_page_de




def help_page_de_view():
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.title("❓ Hilfe & Dokumentation")
    with col_btn:
        st.write("")
        if st.button("⬅️ Zurück zum Rechner", use_container_width=True):
            st.switch_page(calc_page_de)

    st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
            "ersetzt keine professionelle Elektroplanung. "
            "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")

    st.divider()

    # Empty placeholder section for you to fill out
    #
    st.title("Anleitung & Informationen")
    video_de, video_en = st.columns(2)
    with video_de:
        st.header("Video-Tutorial auf Deutsch")
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)
    with video_en:
        st.header("Video-Tutorial auf Englisch")
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)
    st.info("Erklären des Mathematik und wie die Formelle funktionieren im Online-Rechner.")
    st.image(Path(__file__).parent / "photos" / "400VAmps.png")
