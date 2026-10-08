import io
import math
from pathlib import Path
import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Set page config at the entrypoint
st.set_page_config(page_title="Filmlicht & Stromrechner", layout="wide")

# --- Page Definitions ---
def main_calculator():
    # Top header with right-aligned button
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.title("⚡ Filmset Strom- & Lastenrechner")
    with col_btn:
        st.write("")  # Vertical spacing adjustment
        if st.button("❓ Hilfe / Info", use_container_width=True):
            st.switch_page(help_page)

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

            def get_pdf_base(title_text):
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
                elements = []
                styles = getSampleStyleSheet()

                title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor("#1A2B4C"))
                meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=9, leading=13)

                elements.append(Paragraph(f"<b>{title_text}: {project_name}</b>", title_style))
                elements.append(Paragraph(f"<b>Regie / Kurs:</b> {director} | <b>Gaffer / Oberbeleuchter:</b> {gaffer}", meta_style))
                elements.append(Spacer(1, 15))

                return buffer, doc, elements, styles

            def generate_full_pdf():
                buffer, doc, elements, styles = get_pdf_base("Filmset Strom- & Lastenheft")
                summary_data = [
                    ["Gesamt (kW)", "Strom @ 230V", "Scheinleistung", "Min. Aggregat (+25%)", "Empf. Aggregatgröße"],
                    [f"{total_kw:.2f} kW", f"{total_amps_230v} A", f"{total_kva} kVA", f"{min_gen_kva} kVA", f"{suggested_gen_kva} kVA"],
                ]
                sum_table = Table(summary_data, colWidths=[105] * 5)
                sum_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A2B4C")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#F0F2F6")),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ])
                )
                elements.append(sum_table)
                elements.append(Spacer(1, 15))

                elements.append(Paragraph("<b>Phasenverteilung (L1 / L2 / L3 Symmetrierung)</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))
                phase_table_data = [
                    ["Phase", "Wirkleistung (kW)", "Stromstärke @ 230V (A)"],
                    ["L1", f"{(phase_watts['L1']/1000):.2f} kW", f"{(phase_watts['L1']/230):.2f} A"],
                    ["L2", f"{(phase_watts['L2']/1000):.2f} kW", f"{(phase_watts['L2']/230):.2f} A"],
                    ["L3", f"{(phase_watts['L3']/1000):.2f} kW", f"{(phase_watts['L3']/230):.2f} A"],
                ]
                phase_table = Table(phase_table_data, colWidths=[150, 180, 180])
                phase_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ])
                )
                elements.append(phase_table)
                elements.append(Spacer(1, 15))

                elements.append(Paragraph("<b>Aufschlüsselung nach Abteilungen</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))
                dept_table_data = [["Abteilung", "Wirkleistung (kW)", "Strom @ 230V (A)", "Scheinleistung (kVA)"]]
                for _, r in dept_summary.iterrows():
                    dept_table_data.append([
                        str(r["Abteilung"]),
                        f"{r['Gesamt_kW']:.2f} kW",
                        f"{r['Gesamt_Amps_230V']:.2f} A",
                        f"{r['Apparent_kVA']:.2f} kVA",
                    ])
                dept_table = Table(dept_table_data, colWidths=[150, 120, 120, 120])
                dept_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495E")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ])
                )
                elements.append(dept_table)
                elements.append(Spacer(1, 15))

                elements.append(Paragraph("<b>Geräteliste & Einzelverbrauch</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))

                table_data = [["Gerätename", "Abt.", "Menge", "Leistung", "Spannung", "Gesamt (kW)", "Strom (A)"]]
                for _, row in df.iterrows():
                    table_data.append([
                        Paragraph(str(row["Gerätename"]), styles['Normal']),
                        str(row["Abteilung"]),
                        str(int(row["Anzahl"])),
                        f"{int(row['Leistung_W'])} W",
                        f"{int(row['Spannung_V'])} V",
                        f"{(row['Gesamt_W']/1000):.2f} kW",
                        f"{row['Strom_Amps']:.2f} A",
                    ])

                pdf_table = Table(table_data, colWidths=[150, 80, 30, 55, 45, 65, 65])
                pdf_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ])
                )
                elements.append(pdf_table)

                doc.build(elements)
                buffer.seek(0)
                return buffer

            def generate_equipment_list_pdf():
                buffer, doc, elements, styles = get_pdf_base("Equipment-Packliste & Inventar")

                elements.append(Paragraph("<b>Geräteübersicht nach Abteilungen</b>", styles['Heading2']))
                elements.append(Spacer(1, 8))

                for dept in df["Abteilung"].unique():
                    elements.append(Paragraph(f"<b>Abteilung: {dept}</b>", styles['Heading3']))
                    elements.append(Spacer(1, 4))

                    dept_df = df[df["Abteilung"] == dept]
                    table_data = [["Gerätename", "Anzahl / Menge", "Einzelleistung (W)", "Spannung (V)", "Gesamtleistung (kW)"]]
                    for _, row in dept_df.iterrows():
                        table_data.append([
                            Paragraph(str(row["Gerätename"]), styles['Normal']),
                            f"{int(row['Anzahl'])}x",
                            f"{int(row['Leistung_W'])} W",
                            f"{int(row['Spannung_V'])} V",
                            f"{(row['Gesamt_W']/1000):.2f} kW",
                        ])

                    eq_table = Table(table_data, colWidths=[200, 80, 80, 70, 80])
                    eq_table.setStyle(
                        TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 9),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                        ])
                    )
                    elements.append(eq_table)
                    elements.append(Spacer(1, 12))

                doc.build(elements)
                buffer.seek(0)
                return buffer

            def generate_power_plan_pdf():
                buffer, doc, elements, styles = get_pdf_base("Stromverteilungsplan für Elektriker")

                elements.append(Paragraph("<b>Symmetrierung & CEE-Verteiler-Belegung</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))

                phase_data = [
                    ["Phase", "Aktivlast (kW)", "Stromstärke @ 230V (A)"],
                    ["L1", f"{(phase_watts['L1']/1000):.2f} kW", f"{(phase_watts['L1']/230):.2f} A"],
                    ["L2", f"{(phase_watts['L2']/1000):.2f} kW", f"{(phase_watts['L2']/230):.2f} A"],
                    ["L3", f"{(phase_watts['L3']/1000):.2f} kW", f"{(phase_watts['L3']/230):.2f} A"],
                ]
                p_table = Table(phase_data, colWidths=[150, 180, 180])
                p_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A2B4C")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ])
                )
                elements.append(p_table)
                elements.append(Spacer(1, 15))

                elements.append(Paragraph("<b>Detaillierte Zuweisung zu L1, L2, L3</b>", styles['Heading2']))
                elements.append(Spacer(1, 6))

                for p_name in ["L1", "L2", "L3"]:
                    elements.append(Paragraph(f"<b>Zuweisungen für Phase {p_name}:</b>", styles['Heading3']))
                    elements.append(Spacer(1, 4))
                    for item in phases[p_name]:
                        elements.append(Paragraph(f"• {item}", styles['Normal']))
                    elements.append(Spacer(1, 8))

                doc.build(elements)
                buffer.seek(0)
                return buffer

            def generate_dept_summary_pdf():
                buffer, doc, elements, styles = get_pdf_base("Abteilungs-Stromübersicht")

                elements.append(Paragraph("<b>Zusammenfassung der Lasten nach Abteilungen</b>", styles['Heading2']))
                elements.append(Spacer(1, 8))

                dept_table_data = [["Abteilung", "Geräteanzahl", "Wirkleistung (kW)", "Strom @ 230V (A)", "Scheinleistung (kVA)"]]
                for _, r in dept_summary.iterrows():
                    dept_table_data.append([
                        str(r["Abteilung"]),
                        str(r["Geräte_Anzahl"]),
                        f"{r['Gesamt_kW']:.2f} kW",
                        f"{r['Gesamt_Amps_230V']:.2f} A",
                        f"{r['Apparent_kVA']:.2f} kVA",
                    ])

                dept_table = Table(dept_table_data, colWidths=[120, 80, 100, 100, 110])
                dept_table.setStyle(
                    TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#34495E")),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ])
                )
                elements.append(dept_table)

                doc.build(elements)
                buffer.seek(0)
                return buffer

            if pdf_type == "📄 Vollständiges Lastenheft (Komplettübersicht)":
                active_buffer = generate_full_pdf()
                file_suffix = "vollstaendiges_lastenheft"
            elif pdf_type == "📦 Reine Geräteliste (Packliste / Equipment-Inventory)":
                active_buffer = generate_equipment_list_pdf()
                file_suffix = "geraeteliste_packliste"
            elif pdf_type == "⚡ Stromverteilungsplan (Für Elektriker & Gaffer)":
                active_buffer = generate_power_plan_pdf()
                file_suffix = "stromverteilungsplan"
            else:
                active_buffer = generate_dept_summary_pdf()
                file_suffix = "abteilungs_stromuebersicht"

            st.download_button(
                label=f"📥 {pdf_type.split(' ')[1]} herunterladen",
                data=active_buffer,
                file_name=f"{project_name.lower().replace(' ', '_')}_{file_suffix}.pdf",
                mime="application/pdf",
            )


def help_page_view():
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.title("❓ Hilfe & Dokumentation")
        st.info("*Wichtige Hinweise* das Rechner ist ein Werkzeug zur Vorplanung und "
                "ersetzt keine professionelle Elektroplanung. "
                "Bitte prüfe alle Berechnungen und Empfehlungen sorgfältig.")
    with col_btn:
        st.write("")
        if st.button("⬅️ Zurück zum Rechner", use_container_width=True):
            st.switch_page(calc_page)

    st.divider()

    # Empty placeholder section for you to fill out
    #
    st.title("Anleitung & Informationen")
    st.info("Video-Tutorial auf Deutsch")
    embedded_video_url = "https://www.youtube.com/embed/=aYwB4hNAf7A"
    st.info("Erklären des Mathematik und wie die Formelle funktionieren im Online-Rechner.")
    st.image(Path(__file__).parent / "photos" / "400VAmps.png")

# --- Page Routing Setup ---
calc_page = st.Page(main_calculator, title="Stromrechner", icon="⚡", default=True)
help_page = st.Page(help_page_view, title="Hilfe", icon="❓")

# Set position="hidden" to completely remove the sidebar navigation UI
pg = st.navigation([calc_page, help_page], position="hidden")
pg.run()