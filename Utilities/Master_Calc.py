import math

import pandas as pd
import streamlit as st

from Utilities.PDF_Translations import PDF_REPORT_LABELS
from Utilities.Translations import Locale, UI_TEXT as NEW_LOCALE_UI_TEXT
from Utilities.pdf_helpers import generate_pdf_report, get_pdf_font_family
from Utilities.pdf_helpers_De import REPORT_LABELS as DE_REPORT_LABELS
from Utilities.pdf_helpers_En import REPORT_LABELS as EN_REPORT_LABELS


STANDARD_GENERATORS_KVA = [3, 6, 10, 15, 20, 30, 45, 60, 80, 100, 150, 200, 300]

REPORT_LABELS_BY_LANGUAGE = {
    "de": DE_REPORT_LABELS,
    "en": EN_REPORT_LABELS,
    **PDF_REPORT_LABELS,
}

UI_TEXT = {
    "de": {
        "tabs": [
            "📊 Übersicht & Abteilungen",
            "⚡ Einzelauswertung Geräte",
            "🔌 3-Phasen-Abgleich (L1/L2/L3)",
            "📄 PDF-Berichte exportieren",
        ],
        "summary": "Gesamte elektrische Last & Aggregatempfehlungen",
        "total_kw": "Gesamte Wirkleistung",
        "total_amps": "Gesamtstrom @ 230V",
        "total_kva": "Scheinleistung",
        "minimum_generator": "Min. Aggregat (+25%)",
        "recommended_generator": "Empf. Standard-Aggregat",
        "generator_recommendation": (
            "💡 **Aggregat-Empfehlung:** Dein Mindestbedarf inklusive 25% "
            "Sicherheitsreserve liegt bei **{minimum} kVA**. Es wird empfohlen, "
            "das nächstgrößere Standard-Verleihaggregat mit **{recommended} kVA** zu buchen."
        ),
        "departments": "Aufschlüsselung nach Abteilungen",
        "department": "Abteilung",
        "equipment_count": "Anzahl Geräte",
        "active_power": "Wirkleistung (kW)",
        "current": "Stromaufnahme @ 230V",
        "apparent_power": "Scheinleistung (kVA)",
        "device_results": "Berechnete Leistung und Stromstärke pro Gerät",
        "equipment_name": "Gerätename",
        "quantity": "Menge",
        "power_per_item": "Einzelleistung (W)",
        "total_active_power": "Gesamte Wirkleistung",
        "voltage": "Spannung",
        "calculated_current": "Berechneter Strom",
        "phase": "Phase",
        "phase_title": "🔌 Automatischer Drehstrom-Phasenabgleich (L1 / L2 / L3)",
        "phase_caption": (
            "400V-Drehstromgeräte werden automatisch gleichmäßig zu je 1/3 auf "
            "L1, L2 und L3 verteilt. Wechselstromgeräte (230V) werden automatisch "
            "so zugewiesen, dass die Schieflast minimiert wird."
        ),
        "assigned_loads": "**Zugewiesene Lasten:**",
        "create_report": "📄 PDF-Berichte für das Filmset erstellen",
        "choose_report": "Wähle den gewünschten Dokumententyp für den Export aus:",
        "report_type": "Dokumententyp wählen:",
        "download": "📥 {label} herunterladen",
        "three_phase_item": "[400V 3~] ({total}W gesamt → {each}W / {amps}A je Phase)",
        "single_phase_item": "({total}W / {amps}A)",
        "phase_current": "{amps} A @ 230V",
    },
    "en": {
        "tabs": [
            "📊 Overview & Departments",
            "⚡ Equipment Details",
            "🔌 Three-Phase Balancing (L1/L2/L3)",
            "📄 Export PDF Reports",
        ],
        "summary": "Total Electrical Load & Generator Recommendations",
        "total_kw": "Total Active Power",
        "total_amps": "Total Current @ 230 V",
        "total_kva": "Apparent Power",
        "minimum_generator": "Minimum Generator (+25%)",
        "recommended_generator": "Recommended Standard Generator",
        "generator_recommendation": (
            "💡 **Generator recommendation:** Your minimum requirement, including "
            "a 25% safety margin, is **{minimum} kVA**. We recommend booking the "
            "next larger standard generator size: **{recommended} kVA**."
        ),
        "departments": "Department Breakdown",
        "department": "Department",
        "equipment_count": "Equipment Count",
        "active_power": "Active Power (kW)",
        "current": "Current @ 230 V",
        "apparent_power": "Apparent Power (kVA)",
        "device_results": "Calculated Power and Current by Equipment",
        "equipment_name": "Equipment Name",
        "quantity": "Quantity",
        "power_per_item": "Power per Item (W)",
        "total_active_power": "Total Active Power",
        "voltage": "Voltage",
        "calculated_current": "Calculated Current",
        "phase": "Phase",
        "phase_title": "🔌 Automatic Three-Phase Balancing (L1 / L2 / L3)",
        "phase_caption": (
            "400 V three-phase equipment is distributed evenly across L1, L2, "
            "and L3. 230 V single-phase equipment is assigned automatically to "
            "minimize phase imbalance."
        ),
        "assigned_loads": "**Assigned loads:**",
        "create_report": "📄 Create PDF Reports",
        "choose_report": "Choose the type of report to export:",
        "report_type": "Select report type:",
        "download": "📥 Download {label}",
        "three_phase_item": "[400 V 3~] ({total} W total → {each} W / {amps} A per phase)",
        "single_phase_item": "({total} W / {amps} A)",
        "phase_current": "{amps} A @ 230 V",
    },
}
UI_TEXT.update(NEW_LOCALE_UI_TEXT)


def get_next_standard_generator(min_kva: float) -> float:
    """Return the next available standard generator size."""
    for generator in STANDARD_GENERATORS_KVA:
        if generator >= min_kva:
            return generator
    return math.ceil(min_kva)


def render_calculations(
    edited_df: pd.DataFrame,
    *,
    project_name: str,
    director: str,
    gaffer: str,
    language: Locale,
) -> None:
    """Calculate loads and render the localized results and PDF export."""
    if language not in UI_TEXT:
        raise ValueError(f"Unsupported calculator language: {language}")
    if edited_df.empty:
        return

    text = UI_TEXT[language]
    df = edited_df.copy()
    df["Gesamt_W"] = df["Anzahl"] * df["Leistung_W"]
    df["Strom_Amps"] = (
        df["Gesamt_W"] / (df["Spannung_V"] * df["Power_Factor"])
    ).round(2)
    df["Apparent_VA"] = (df["Gesamt_W"] / df["Power_Factor"]).round(2)

    total_watts = df["Gesamt_W"].sum()
    total_kw = total_watts / 1000
    total_amps_230v = round(total_watts / 230, 2)
    total_kva = round(df["Apparent_VA"].sum() / 1000, 2)
    min_gen_kva = round(total_kva * 1.25, 2)
    suggested_gen_kva = get_next_standard_generator(min_gen_kva)

    phases: dict[str, list[str]] = {"L1": [], "L2": [], "L3": []}
    phase_watts = {"L1": 0.0, "L2": 0.0, "L3": 0.0}

    for _, row in df[df["Spannung_V"] == 400].iterrows():
        third_w = row["Gesamt_W"] / 3.0
        third_amps = round(third_w / 230, 2)
        item = f"{row['Gerätename']} {text['three_phase_item'].format(total=int(row['Gesamt_W']), each=int(third_w), amps=third_amps)}"
        for phase in phases:
            phases[phase].append(item)
            phase_watts[phase] += third_w

    single_phase_devices = df[df["Spannung_V"] == 230].sort_values(
        by="Gesamt_W", ascending=False
    )
    for _, row in single_phase_devices.iterrows():
        phase = min(phase_watts, key=phase_watts.get)
        phases[phase].append(
            f"{row['Gerätename']} "
            f"{text['single_phase_item'].format(total=int(row['Gesamt_W']), amps=row['Strom_Amps'])}"
        )
        phase_watts[phase] += row["Gesamt_W"]

    dept_summary = (
        df.groupby("Abteilung")
        .agg(
            Geräte_Anzahl=("Anzahl", "sum"),
            Gesamt_kW=("Gesamt_W", lambda values: round(values.sum() / 1000, 2)),
            Gesamt_Amps_230V=("Gesamt_W", lambda values: round(values.sum() / 230, 2)),
            Apparent_kVA=("Apparent_VA", lambda values: round(values.sum() / 1000, 2)),
        )
        .reset_index()
    )

    st.divider()
    tab_summary, tab_devices, tab_three_phase, tab_export = st.tabs(text["tabs"])

    with tab_summary:
        st.subheader(text["summary"])
        metrics = st.columns(5)
        metric_data = [
            (text["total_kw"], f"{total_kw:.2f} kW"),
            (text["total_amps"], f"{total_amps_230v} A"),
            (text["total_kva"], f"{total_kva} kVA"),
            (text["minimum_generator"], f"{min_gen_kva} kVA"),
            (text["recommended_generator"], f"{suggested_gen_kva} kVA"),
        ]
        for column, (label, value) in zip(metrics, metric_data):
            column.metric(label, value)

        st.info(
            text["generator_recommendation"].format(
                minimum=min_gen_kva,
                recommended=suggested_gen_kva,
            )
        )
        st.subheader(text["departments"])
        st.dataframe(
            dept_summary,
            column_config={
                "Abteilung": text["department"],
                "Geräte_Anzahl": text["equipment_count"],
                "Gesamt_kW": st.column_config.NumberColumn(
                    text["active_power"], format="%.2f kW"
                ),
                "Gesamt_Amps_230V": st.column_config.NumberColumn(
                    text["current"], format="%.2f A"
                ),
                "Apparent_kVA": st.column_config.NumberColumn(
                    text["apparent_power"], format="%.2f kVA"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab_devices:
        st.subheader(text["device_results"])
        display_df = df[
            [
                "Gerätename",
                "Abteilung",
                "Anzahl",
                "Leistung_W",
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
                "Gerätename": text["equipment_name"],
                "Abteilung": text["department"],
                "Anzahl": text["quantity"],
                "Leistung_W": st.column_config.NumberColumn(
                    text["power_per_item"], format="%d W"
                ),
                "Gesamt_kW": st.column_config.NumberColumn(
                    text["total_active_power"], format="%.2f kW"
                ),
                "Spannung_V": st.column_config.NumberColumn(
                    text["voltage"], format="%d V"
                ),
                "Strom_Amps": st.column_config.NumberColumn(
                    text["calculated_current"], format="%.2f A"
                ),
                "Apparent_kVA": st.column_config.NumberColumn(
                    text["apparent_power"], format="%.2f kVA"
                ),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab_three_phase:
        st.subheader(text["phase_title"])
        st.caption(text["phase_caption"])
        phase_columns = st.columns(3)
        for column, phase in zip(phase_columns, ("L1", "L2", "L3")):
            with column:
                phase_kw = phase_watts[phase] / 1000.0
                phase_amps = round(phase_watts[phase] / 230.0, 2)
                st.metric(
                    f"{text['phase']} {phase}",
                    f"{phase_kw:.2f} kW",
                    text["phase_current"].format(amps=phase_amps),
                )
                st.write(text["assigned_loads"])
                for device in phases[phase]:
                    st.write(f"- {device}")

    with tab_export:
        st.subheader(text["create_report"])
        st.write(text["choose_report"])
        report_labels = REPORT_LABELS_BY_LANGUAGE[language]
        report_options = list(report_labels["report_types"])
        pdf_type = st.selectbox(text["report_type"], options=report_options)
        report_arguments = {
            "pdf_type": pdf_type,
            "project_name": project_name,
            "director": director,
            "gaffer": gaffer,
            "df": df,
            "dept_summary": dept_summary,
            "total_kw": total_kw,
            "total_amps_230v": total_amps_230v,
            "total_kva": total_kva,
            "min_gen_kva": min_gen_kva,
            "suggested_gen_kva": suggested_gen_kva,
            "phase_watts": phase_watts,
            "phases": phases,
        }
        regular_font, bold_font = get_pdf_font_family(language)
        active_buffer, file_suffix = generate_pdf_report(
            **report_arguments,
            labels=report_labels,
            regular_font=regular_font,
            bold_font=bold_font,
            right_to_left=language in {"ar", "he"},
        )

        st.download_button(
            label=text["download"].format(label=pdf_type.split(" ", 1)[-1]),
            data=active_buffer,
            file_name=f"{project_name.lower().replace(' ', '_')}_{file_suffix}.pdf",
            mime="application/pdf",
        )
