from pathlib import Path

import streamlit as st

from Utilities.Language_Selection import apply_header_styles, language_selection


def Help_Page_View_De(calc_page_de, help_page_de, help_page_en, language_pages=None):
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
            language_selection(
                help_page_de,
                help_page_en,
                "Deutsch",
                additional_pages=language_pages,
            )
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
            st.title("Anleitung & Informationen")
        with tutorial_video_title:
            st.title("Video-Tutorial auf Deutsch")
    
    tutorial_text, tutorial_video = st.columns([2.5, 1], wrap=False)
            
    with tutorial_text:
        st.write(
        "Um die elektrische Last zu berechnen, müssen Sie alle Geräte an Ihrem"
        " Filmset angeben. Als Erstes erstellen Sie eine Inventarliste aller"
        " Geräte samt ihren technischen Daten. Wichtig sind die Leistung pro"
        " Gerät in Watt, die Anzahl, die Spannung und der Leistungsfaktor."
        " Verwenden Sie 230 V für einphasige und 400 V für dreiphasige Geräte."
        " Ordnen Sie bei größeren Sets jedes Gerät außerdem einer Abteilung"
        " zu, z. B. Produktion, Ton, Video, Catering oder Licht.\n\nSie können"
        " diese Liste direkt in"
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
        " der Geräte auf die drei Phasen. Als Planungsziel sollte die"
        " Abweichung zwischen den Phasen möglichst unter 10 % (in kVA) liegen."
        " Lassen Sie die endgültige Verteilung von einer Fachkraft prüfen."
        "\n\nIm letzten Reiter"
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
        st.video("https://www.youtube.com/watch?v=aYwB4hNAf7A", width="stretch")
        st.image(
            Path(__file__).resolve().parents[2] / "photos" / "400VAmps.png",
            width="stretch",
        )
        st.image(
            Path(__file__).resolve().parents[2] / "photos" / "230VAmps.png",
            width="stretch",
        )
        st.image(
            Path(__file__).resolve().parents[2] / "photos" / "kW.pF.kVA.png",
            width="stretch",
        )
        st.image(
            Path(__file__).resolve().parents[2] / "photos" / "kWx1000.W.png",
            width="stretch",
        )

    st.subheader("So schätzt der Rechner die elektrische Last am Set")
    st.write(
        "Jede Zeile der Geräteliste steht für einen Teil der Stromplanung am "
        "Set – zum Beispiel eine Gruppe LED-Scheinwerfer, ein Kamerapaket, "
        "eine Tonanlage oder Catering-Geräte. Der Rechner multipliziert die "
        "Anzahl mit der Leistung eines einzelnen Geräts. So erhält er die "
        "Gesamtleistung der Zeile in Watt (W). Alle Zeilen werden addiert und "
        "durch 1.000 geteilt: Das ergibt die Wirkleistung des Sets in "
        "Kilowatt (kW).\n\n"
        "Der Rechner schätzt den Strom einer Zeile so: Gesamtleistung "
        "der Zeile / (Spannung x Leistungsfaktor). Die Scheinleistung wird "
        "berechnet als: Gesamtleistung der Zeile / Leistungsfaktor. Die "
        "Scheinleistung aller Zeilen wird addiert und durch 1.000 geteilt, "
        "um den Wert in Kilovoltampere (kVA) anzuzeigen. Der Leistungsfaktor "
        "(PF oder cos phi) beschreibt den Unterschied zwischen Wirkleistung "
        "(kW), die tatsächlich Arbeit verrichtet, und Scheinleistung (kVA), "
        "die für die Auslegung von Generator und Stromversorgung wichtig ist."
        "\n\n"
        "Diese Stromformel ist eine Schätzung für einphasige Geräte. Bei "
        "400-V-Drehstromgeräten sollten Sie den Nennstrom laut Hersteller "
        "verwenden oder den Leiterstrom von einer Elektrofachkraft prüfen "
        "lassen; in der Stromschätzung des Rechners wird der Drehstromfaktor "
        "nicht berücksichtigt.\n\n"
        "Beispiel: Vier LED-Scheinwerfer mit je 420 W ergeben zusammen "
        "1.680 W beziehungsweise 1,68 kW. Bei 230 V und einem Leistungsfaktor "
        "von 0,99 beträgt der geschätzte Strom 1.680 / (230 x 0,99), also "
        "rund 7,38 A. Die Scheinleistung liegt bei etwa 1,70 kVA.\n\n"
        "Der Gesamtstrom in der Übersicht bei 230 V ist ein vereinfachter "
        "Vergleichswert: Gesamtwatt / 230. Er entspricht nicht der Summe der "
        "tatsächlichen Ströme von Geräten mit unterschiedlichen Spannungen. "
        "Für die Generator-Empfehlung schlägt der Rechner 25 % auf die gesamte "
        "Scheinleistung in kVA auf und empfiehlt eine Standardgröße, die "
        "mindestens diesem Wert entspricht, sofern eine passende Größe in "
        "der Liste verfügbar ist.\n\n"
        "Im Phasenabgleich wird jede 400-V-Drehstromlast gleichmäßig auf "
        "L1, L2 und L3 verteilt. Die 230-V-Einphasenlasten werden von der "
        "größten zur kleinsten sortiert und nacheinander der Phase mit der "
        "geringsten bisherigen Wirkleistung zugeordnet. Das ist eine "
        "Planungsschätzung auf Basis der Wattwerte. Anlaufströme, wechselnde "
        "Lasten, Kabel- und Sicherungsgrenzen sowie alle Auswirkungen des "
        "Leistungsfaktors im realen Betrieb werden damit nicht abgebildet. "
        "Prüfen Sie Gerätedaten und endgültige Stromverteilung vor dem Dreh "
        "mit einer Elektrofachkraft."
    )
    