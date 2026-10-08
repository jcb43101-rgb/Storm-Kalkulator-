from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import apply_header_styles, language_selection


def Help_Page_View_De(calc_page_de, help_page_de, help_page_en):
    apply_header_styles()
    col_title, col_controls = st.columns(
        [0.56, 0.44], vertical_alignment="bottom", wrap=False
    )
    with col_title:
        st.title("❓ Hilfe & Dokumentation")
    with col_controls:
        with st.container(
            horizontal=True,
            horizontal_alignment="right",
            vertical_alignment="bottom",
            gap="small",
            key="header_controls",
        ):
            language_selection(help_page_de, help_page_en, "Deutsch")
            if st.button(
                "Rechner",
                width="content",
                key="header_navigation_button",
            ):
                st.switch_page(calc_page_de)

    st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
            "ersetzt keine professionelle Elektroplanung. "
            "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")

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
        st.write(
        "Um die elektrische Last zu berechnen, müssen Sie alle Geräte an Ihrem"
        " Filmset angeben. Als Erstes erstellen Sie eine Inventarliste aller"
        " Geräte samt ihren technischen Daten. Die wichtigsten Angaben sind:"
        " Wattzahl, Stromstärke (Ampere), ob es sich um 1- oder 3-phasigen Strom"
        " handelt und ob Wechselstrom (AC) oder Gleichstrom (DC) verwendet"
        " wird. Geben Sie außerdem die Anzahl der jeweiligen Geräte an und bei"
        " größeren Sets das entsprechende Department (z. B. Produktion, Ton,"
        " Video, Catering oder Licht).\n\nSie können diese Liste direkt in"
        " unserem Online-Rechner erstellen. Beachten Sie jedoch, dass die Daten"
        " nicht automatisch gespeichert werden – beim Aktualisieren der Seite"
        " gehen Ihre Eingaben verloren! Alternativ können Sie eine CSV-Datei mit"
        " den Gerätedaten erstellen und hochladen, um den Rechner automatisch"
        " auszufüllen.\n\nWährend Sie die Geräteliste im Rechner ausfüllen,"
        " aktualisiert unser mathematischer Algorithmus automatisch die"
        " Berechnungen am Seitenende, um alle Geräte zu berücksichtigen. Sie"
        " können die Daten anschließend nach verschiedenen Ansichten sortieren,"
        " etwa nach technischen Daten pro Gerät oder nach Department.\n\nWenn"
        " Sie Drehstrom (3 Phasen) oder Generatoren nutzen, finden Sie"
        " außerdem einen Reiter mit Empfehlungen zur gleichmäßigen Aufteilung"
        " der Geräte auf die drei Phasen. Die Abweichung zwischen den einzelnen"
        " Phasen sollte maximal 10 % (in kVA) betragen.\n\nIm letzten Reiter"
        " können Sie eine PDF-Datei Ihrer Geräteliste exportieren. Es stehen"
        " vier verschiedene Layouts zur Auswahl – wählen Sie einfach das"
        " passende (oder alle vier) für Ihren Bedarf aus. Die PDFs können Sie"
        " anschließend ausdrucken und an Ihr Team verteilen!\n\nDie genauen"
        " mathematischen Formeln unseres Algorithmus finden Sie"
        " unten.\n\nToi, toi, toi!"
    )
    st.info(
        "Erfahren Sie mehr über die Mathematik und die Formeln hinter unserem"
        " Online-Rechner."
    )
        
    with tutorial_video:
            st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width=500)
            st.image(Path(__file__).resolve().parents[2] / "photos" / "400VAmps.png", width=500)
            st.image(Path(__file__).resolve().parents[2] / "photos" / "230VAmps.png", width=500)
            st.image(Path(__file__).resolve().parents[2] / "photos" / "kW.pF.kVA.png", width=500)
            st.image(Path(__file__).resolve().parents[2] / "photos" / "kWx1000.W.png", width=500)
    