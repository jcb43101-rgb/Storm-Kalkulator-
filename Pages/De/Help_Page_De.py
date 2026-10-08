from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import language_selection


def Help_Page_View_De(calc_page_de, help_page_de, help_page_en):
    col_title, col_btn, col_language = st.columns([0.68, 0.16, 0.16])
    with col_title:
        st.title("❓ Hilfe & Dokumentation")
    with col_btn:
        st.write("")
        if st.button("⬅️ Zurück zum Rechner", use_container_width=True):
            st.switch_page(calc_page_de)
    with col_language:
        language_selection(help_page_de, help_page_en, "Deutsch")

    st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
            "ersetzt keine professionelle Elektroplanung. "
            "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")

    st.divider()

    st.title("Anleitung & Informationen")
    video_de, video_en = st.columns(2)
    with video_de:
        st.header("Video-Tutorial auf Deutsch")
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)
    st.info("Erklären des Mathematik und wie die Formelle funktionieren im Online-Rechner.")
    st.image(Path(__file__).resolve().parents[2] / "photos" / "400VAmps.png")
