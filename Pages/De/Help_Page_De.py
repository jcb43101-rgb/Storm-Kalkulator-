from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import language_selection


def Help_Page_View_De(calc_page_de, help_page_de, help_page_en):
    col_title, col_language, col_btn = st.columns(
        [0.70, 0.20, 0.10], vertical_alignment="bottom", wrap=False
    )
    with col_title:
        st.title("❓ Hilfe & Dokumentation")
    with col_language:
        language_selection(help_page_de, help_page_en, "Deutsch")
    with col_btn:
        if st.button("Zurück", width="content", key="header_navigation_button"):
            st.switch_page(calc_page_de)

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
