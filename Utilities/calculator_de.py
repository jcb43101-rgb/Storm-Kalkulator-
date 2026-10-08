import math

import pandas as pd
import streamlit as st
from Utilities.pdf_helpers import generate_pdf_report_De as generate_pdf_report


def main_calculator_de(help_page_de):
    # Top header with right-aligned button
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.title("⚡ Filmset Strom- & Lastenrechner")
    with col_btn:
        st.write("")  # Vertical spacing adjustment
        if st.button("❓ Hilfe / Info", use_container_width=True):
            st.switch_page(help_page_de)

    st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
                        "ersetzt keine professionelle Elektroplanung. "
                        "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")

    st.write(
        "Füge deine Set-Geräte unten ein, um Ein- und Drehstromlasten zu berechnen, "
        "Abteilungsanalysen einzusehen, Phasen (L1, L2, L3) automatisch abzugleichen und passende PDF-Berichte zu erstellen."
    )

    # --- Standard-Generatorgrößen (in kVA) ---
    STANDARD_GENERATORS_KVA = [3, 6, 10, 15, 20, 30, 45, 60, 80, 100, 150, 200, 300]

    def get_next_standard_generator(min_kva: float) -> float:
        """Ermittelt die nächstgrößere Standard-Aggregatgröße."""
        for gen in STANDARD_GENERATORS_KVA:
            if gen >= min_kva:
                return gen
        return math.ceil(min_kva)

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

    # --- Berechnungen ---
    if not edited_df.empty:
        df = edited_df.copy()

        # Core Calculations
        df["Gesamt_W"] = df["Anzahl"] * df["Leistung_W"]
        df["Strom_Amps"] = (df["Gesamt_W"] / (df["Spannung_V"] * df["Power_Factor"])).round(2)
        df["Apparent_VA"] = (df["Gesamt_W"] / df["Power_Factor"]).round(2)

        total_watts = df["Gesamt_W"].sum()
        total_kw = total_watts / 1000
        total_amps_230v = round(total_watts / 230, 2)
        total_kva = round(df["Apparent_VA"].sum() / 1000, 2)

        # Aggregatberechnungen
        min_gen_kva = round(total_kva * 1.25, 2)
        suggested_gen_kva = get_next_standard_generator(min_gen_kva)

        # --- 3-Phasen-Symmetrierung (L1 / L2 / L3) ---
        phases = {"L1": [], "L2": [], "L3": []}
        phase_watts = {"L1": 0.0, "L2": 0.0, "L3": 0.0}

        # 1. Drehstromgeräte (400V)
        v400_devices = df[df["Spannung_V"] == 400]
        for _, row in v400_devices.iterrows():
            third_w = row["Gesamt_W"] / 3.0
            third_amps = round(third_w / 230, 2)
            item_str = f"{row['Gerätename']} [400V 3~] ({int(row['Gesamt_W'])}W gesamt → {int(third_w)}W / {third_amps}A je Phase)"
            for p in ["L1", "L2", "L3"]:
                phases[p].append(item_str)
                phase_watts[p] += third_w

        # 2. Wechselstromgeräte (230V)
        v230_devices = df[df["Spannung_V"] == 230].sort_values(by="Gesamt_W", ascending=False)
        for _, row in v230_devices.iterrows():
            min_p = min(phase_watts, key=phase_watts.get)
            phases[min_p].append(f"{row['Gerätename']} ({int(row['Gesamt_W'])}W / {row['Strom_Amps']}A)")
            phase_watts[min_p] += row["Gesamt_W"]

        st.divider()

        # Reiter zur strukturierten Ansicht
        tab_summary, tab_devices, tab_three_phase, tab_export = st.tabs(
            ["📊 Übersicht & Abteilungen", "⚡ Einzelauswertung Geräte", "🔌 3-Phasen-Abgleich (L1/L2/L3)", "📄 PDF-Berichte Exportieren"]
        )

        with tab_summary:
            st.subheader("Gesamte elektrische Last & Aggregatempfehlungen")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Gesamte Wirkleistung", f"{total_kw:.2f} kW")
            m2.metric("Gesamtstrom @ 230V", f"{total_amps_230v} A")
            m3.metric("Scheinleistung", f"{total_kva} kVA")
            m4.metric("Min. Aggregat (+25%)", f"{min_gen_kva} kVA")
            m5.metric("Empf. Standard-Aggregat", f"{suggested_gen_kva} kVA")

            st.info(
                f"💡 **Aggregat-Empfehlung:** Dein Mindestbedarf inklusive 25% Sicherheitsreserve liegt bei **{min_gen_kva} kVA**. "
                f"Es wird empfohlen, das nächstgrößere Standard-Verleihaggregat mit **{suggested_gen_kva} kVA** zu buchen."
            )

            st.subheader("Aufschlüsselung nach Abteilungen")
            dept_summary = (
                df.groupby("Abteilung")
                .agg(
                    Geräte_Anzahl=("Anzahl", "sum"),
                    Gesamt_kW=("Gesamt_W", lambda x: round(x.sum() / 1000, 2)),
                    Gesamt_Amps_230V=("Gesamt_W", lambda x: round(x.sum() / 230, 2)),
                    Apparent_kVA=("Apparent_VA", lambda x: round(x.sum() / 1000, 2)),
                )
                .reset_index()
            )

            st.dataframe(
                dept_summary,
                column_config={
                    "Abteilung": "Abteilung",
                    "Geräte_Anzahl": "Anzahl Geräte",
                    "Gesamt_kW": st.column_config.NumberColumn("Wirkleistung (kW)", format="%.2f kW"),
                    "Gesamt_Amps_230V": st.column_config.NumberColumn("Stromaufnahme @ 230V", format="%.2f A"),
                    "Apparent_kVA": st.column_config.NumberColumn("Scheinleistung (kVA)", format="%.2f kVA"),
                },
                use_container_width=True,
                hide_index=True,
            )

        with tab_devices:
            st.subheader("Berechnete Leistung und Stromstärke pro Gerät")
            display_df = df[
                [
                    "Gerätename",
                    "Abteilung",
                    "Anzahl",
                    "Leistung_W",
                    "Power_Factor",
                    "Spannung_V",
                    "Gesamt_W",
                    "Strom_Amps",
                    "Apparent_VA",
                ]
            ].copy()

            display_df["Gesamt_kW"] = (display_df["Gesamt_W"] / 1000).round(2)
            display_df["Apparent_kVA"] = (display_df["Apparent_VA"] / 1000).round(2)

            st.dataframe(
                display_df[
                    [
                        "Gerätename",
                        "Abteilung",
                        "Anzahl",
                        "Leistung_W",
                        "Gesamt_kW",
                        "Spannung_V",
                        "Strom_Amps",
                        "Apparent_kVA",
                    ]
                ],
                column_config={
                    "Gerätename": "Gerätename",
                    "Abteilung": "Abteilung",
                    "Anzahl": "Menge",
                    "Leistung_W": st.column_config.NumberColumn("Einzelleistung (W)", format="%d W"),
                    "Gesamt_kW": st.column_config.NumberColumn("Gesamte Wirkleistung", format="%.2f kW"),
                    "Spannung_V": st.column_config.NumberColumn("Spannung", format="%d V"),
                    "Strom_Amps": st.column_config.NumberColumn("Berechneter Strom", format="%.2f A"),
                    "Apparent_kVA": st.column_config.NumberColumn("Scheinleistung", format="%.2f kVA"),
                },
                use_container_width=True,
                hide_index=True,
            )

        with tab_three_phase:
            st.subheader("🔌 Automatischer Drehstrom-Phasenabgleich (L1 / L2 / L3)")
            st.caption(
                "400V-Drehstromgeräte werden automatisch gleichmäßig zu je 1/3 auf L1, L2 und L3 verteilt. "
                "Wechselstromgeräte (230V) werden automatisch so zugewiesen, dass die Schieflast minimiert wird."
            )

            p_col1, p_col2, p_col3 = st.columns(3)
            for col, phase_name in zip([p_col1, p_col2, p_col3], ["L1", "L2", "L3"]):
                with col:
                    p_kw = phase_watts[phase_name] / 1000.0
                    p_amps = round(phase_watts[phase_name] / 230.0, 2)
                    st.metric(f"Phase {phase_name}", f"{p_kw:.2f} kW", f"{p_amps} A @ 230V")
                    st.write("**Zugewiesene Lasten:**")
                    for dev in phases[phase_name]:
                        st.write(f"- {dev}")

        with tab_export:
            st.subheader("📄 PDF-Berichte für das Filmset erstellen")
            st.write("Wähle den gewünschten Dokumententyp für den Export aus:")

            pdf_type = st.selectbox(
                "Dokumententyp wählen:",
                options=[
                    "📄 Vollständiges Lastenheft (Komplettübersicht)",
                    "📦 Reine Geräteliste (Packliste / Equipment-Inventory)",
                    "⚡ Stromverteilungsplan (Für Elektriker & Gaffer)",
                    "📊 Abteilungs-Kosten & Lastenübersicht",
                ],
            )

            active_buffer, file_suffix = generate_pdf_report(
                pdf_type=pdf_type,
                project_name=project_name,
                director=director,
                gaffer=gaffer,
                df=df,
                dept_summary=dept_summary,
                total_kw=total_kw,
                total_amps_230v=total_amps_230v,
                total_kva=total_kva,
                min_gen_kva=min_gen_kva,
                suggested_gen_kva=suggested_gen_kva,
                phase_watts=phase_watts,
                phases=phases,
            )

            st.download_button(
                label=f"📥 {pdf_type.split(' ')[1]} herunterladen",
                data=active_buffer,
                file_name=f"{project_name.lower().replace(' ', '_')}_{file_suffix}.pdf",
                mime="application/pdf",
            )


