import io

import pandas as pd

from Utilities.pdf_helpers_De import ReportLabels, generate_pdf_report


REPORT_LABELS: ReportLabels = {
    "director": "Regie / Kurs",
    "gaffer": "Gaffer / Oberbeleuchter",
    "full_title": "Filmset Strom- & Lastenheft",
    "total": "Gesamt (kW)",
    "current": "Strom @ 230V",
    "apparent": "Scheinleistung",
    "minimum_generator": "Min. Aggregat (+25%)",
    "recommended_generator": "Empf. Aggregatgröße",
    "phase_distribution": "Phasenverteilung (L1 / L2 / L3 Symmetrierung)",
    "active_power": "Wirkleistung (kW)",
    "current_230": "Stromstärke @ 230V (A)",
    "department_breakdown": "Aufschlüsselung nach Abteilungen",
    "department": "Abteilung",
    "department_apparent": "Scheinleistung (kVA)",
    "equipment_consumption": "Geräteliste & Einzelverbrauch",
    "equipment_name": "Gerätename",
    "department_abbreviation": "Abt.",
    "quantity": "Menge",
    "power": "Leistung",
    "voltage": "Spannung",
    "total_kw": "Gesamt (kW)",
    "current_a": "Strom (A)",
    "equipment_title": "Equipment-Packliste & Inventar",
    "equipment_overview": "Geräteübersicht nach Abteilungen",
    "department_count": "Geräteanzahl",
    "power_per_item": "Einzelleistung (W)",
    "voltage_v": "Spannung (V)",
    "total_power_kw": "Gesamtleistung (kW)",
    "distribution_title": "Stromverteilungsplan für Elektriker",
    "balancing": "Symmetrierung & CEE-Verteiler-Belegung",
    "detailed_assignment": "Detaillierte Zuweisung zu L1, L2, L3",
    "phase_assignment": "Zuweisungen für Phase",
    "department_report_title": "Abteilungs-Stromübersicht",
    "load_summary": "Zusammenfassung der Lasten nach Abteilungen",
    "report_types": {
        "📄 Vollständiges Lastenheft (Komplettübersicht)": (
            "full",
            "vollstaendiges_lastenheft",
        ),
        "📦 Reine Geräteliste (Packliste / Equipment-Inventory)": (
            "equipment",
            "geraeteliste_packliste",
        ),
        "⚡ Stromverteilungsplan (Für Elektriker & Gaffer)": (
            "power",
            "stromverteilungsplan",
        ),
        "📊 Abteilungs-Kosten & Lastenübersicht": (
            "department",
            "abteilungs_stromuebersicht",
        ),
    },
}


def generate_pdf_report_De(
    *,
    pdf_type: str,
    project_name: str,
    director: str,
    gaffer: str,
    df: pd.DataFrame,
    dept_summary: pd.DataFrame,
    total_kw: float,
    total_amps_230v: float,
    total_kva: float,
    min_gen_kva: float,
    suggested_gen_kva: float,
    phase_watts: dict[str, float],
    phases: dict[str, list[str]],
) -> tuple[io.BytesIO, str]:
    return generate_pdf_report(
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
        labels=REPORT_LABELS,
    )
