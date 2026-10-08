import io

import pandas as pd

from Utilities.pdf_helpers_De import ReportLabels, generate_pdf_report


REPORT_LABELS: ReportLabels = {
    "director": "Director / Course",
    "gaffer": "Gaffer",
    "full_title": "Film Set Power & Load Report",
    "total": "Total (kW)",
    "current": "Current @ 230 V",
    "apparent": "Apparent Power",
    "minimum_generator": "Minimum Generator (+25%)",
    "recommended_generator": "Recommended Generator Size",
    "phase_distribution": "Phase Distribution (L1 / L2 / L3 Balancing)",
    "active_power": "Active Power (kW)",
    "current_230": "Current @ 230 V (A)",
    "department_breakdown": "Breakdown by Department",
    "department": "Department",
    "department_apparent": "Apparent Power (kVA)",
    "equipment_consumption": "Equipment List & Individual Consumption",
    "equipment_name": "Equipment Name",
    "department_abbreviation": "Dept.",
    "quantity": "Quantity",
    "power": "Power",
    "voltage": "Voltage",
    "total_kw": "Total (kW)",
    "current_a": "Current (A)",
    "equipment_title": "Equipment Packing List & Inventory",
    "equipment_overview": "Equipment Overview by Department",
    "department_count": "Equipment Count",
    "power_per_item": "Power per Item (W)",
    "voltage_v": "Voltage (V)",
    "total_power_kw": "Total Power (kW)",
    "distribution_title": "Power Distribution Plan for Electricians",
    "balancing": "Phase Balancing & CEE Distribution Board Assignment",
    "detailed_assignment": "Detailed Assignment to L1, L2, and L3",
    "phase_assignment": "Assignments for Phase",
    "department_report_title": "Department Power Summary",
    "load_summary": "Load Summary by Department",
    "report_types": {
        "📄 Complete Load Report (Full Summary)": (
            "full",
            "complete_load_report",
        ),
        "📦 Equipment List (Packing / Inventory)": (
            "equipment",
            "equipment_packing_list",
        ),
        "⚡ Power Distribution Plan (For Electricians & Gaffers)": (
            "power",
            "power_distribution_plan",
        ),
        "📊 Department Load Summary": (
            "department",
            "department_power_summary",
        ),
    },
}


def generate_pdf_report_En(
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
