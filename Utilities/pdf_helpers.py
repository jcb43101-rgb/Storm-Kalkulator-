import io
from typing import TypedDict
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportLabels(TypedDict):
    director: str
    gaffer: str
    full_title: str
    total: str
    current: str
    apparent: str
    minimum_generator: str
    recommended_generator: str
    phase_distribution: str
    active_power: str
    current_230: str
    department_breakdown: str
    department: str
    department_apparent: str
    equipment_consumption: str
    equipment_name: str
    department_abbreviation: str
    quantity: str
    power: str
    voltage: str
    total_kw: str
    current_a: str
    equipment_title: str
    equipment_overview: str
    department_count: str
    power_per_item: str
    voltage_v: str
    total_power_kw: str
    distribution_title: str
    balancing: str
    detailed_assignment: str
    phase_assignment: str
    department_report_title: str
    load_summary: str
    report_types: dict[str, tuple[str, str]]


def _table(rows: list[list[object]], widths: list[int]) -> Table:
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _paragraph(value: object, styles: dict[str, object]) -> Paragraph:
    return Paragraph(escape(str(value)), styles["BodyText"])


def generate_pdf_report(
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
    labels: ReportLabels,
) -> tuple[io.BytesIO, str]:
    try:
        report_kind, file_suffix = labels["report_types"][pdf_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported PDF report type: {pdf_type}") from exc

    title_key = {
        "full": "full_title",
        "equipment": "equipment_title",
        "power": "distribution_title",
        "department": "department_report_title",
    }[report_kind]
    styles = getSampleStyleSheet()
    buffer = io.BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
        title=f"{labels[title_key]} - {project_name}",
    )
    story = [
        Paragraph(escape(labels[title_key]), styles["Title"]),
        Paragraph(escape(project_name), styles["Heading2"]),
        Paragraph(
            f"{escape(labels['director'])}: {escape(director)}"
            f"&nbsp;&nbsp;&nbsp; {escape(labels['gaffer'])}: {escape(gaffer)}",
            styles["BodyText"],
        ),
        Spacer(1, 14),
    ]

    def append_department_table() -> None:
        rows: list[list[object]] = [
            [
                labels["department"],
                labels["active_power"],
                labels["current_230"],
                labels["department_apparent"],
            ]
        ]
        for _, row in dept_summary.iterrows():
            rows.append(
                [
                    _paragraph(row["Abteilung"], styles),
                    f"{row['Gesamt_kW']:.2f} kW",
                    f"{row['Gesamt_Amps_230V']:.2f} A",
                    f"{row['Apparent_kVA']:.2f} kVA",
                ]
            )
        story.append(_table(rows, [145, 120, 120, 120]))

    def append_equipment_table(equipment: pd.DataFrame) -> None:
        rows: list[list[object]] = [
            [
                labels["equipment_name"],
                labels["department_abbreviation"],
                labels["quantity"],
                labels["power"],
                labels["voltage"],
                labels["total_kw"],
                labels["current_a"],
            ]
        ]
        for _, row in equipment.iterrows():
            rows.append(
                [
                    _paragraph(row["Gerätename"], styles),
                    _paragraph(row["Abteilung"], styles),
                    str(int(row["Anzahl"])),
                    f"{int(row['Leistung_W'])} W",
                    f"{int(row['Spannung_V'])} V",
                    f"{row['Gesamt_W'] / 1000:.2f} kW",
                    f"{row['Strom_Amps']:.2f} A",
                ]
            )
        story.append(_table(rows, [130, 76, 38, 60, 55, 65, 65]))

    if report_kind == "full":
        story.append(
            _table(
                [
                    [labels["total"], f"{total_kw:.2f} kW"],
                    [labels["current"], f"{total_amps_230v:.2f} A"],
                    [labels["apparent"], f"{total_kva:.2f} kVA"],
                    [labels["minimum_generator"], f"{min_gen_kva:.2f} kVA"],
                    [labels["recommended_generator"], f"{suggested_gen_kva:.2f} kVA"],
                ],
                [260, 263],
            )
        )
        story.extend(
            [
                Spacer(1, 14),
                Paragraph(escape(labels["phase_distribution"]), styles["Heading2"]),
                _table(
                    [
                        [labels["phase_assignment"], labels["active_power"], labels["current_230"]],
                        *[
                            [
                                phase,
                                f"{phase_watts[phase] / 1000:.2f} kW",
                                f"{phase_watts[phase] / 230:.2f} A",
                            ]
                            for phase in ("L1", "L2", "L3")
                        ],
                    ],
                    [150, 180, 180],
                ),
                Spacer(1, 14),
                Paragraph(escape(labels["department_breakdown"]), styles["Heading2"]),
            ]
        )
        append_department_table()
        story.extend(
            [
                Spacer(1, 14),
                Paragraph(escape(labels["equipment_consumption"]), styles["Heading2"]),
            ]
        )
        append_equipment_table(df)
    elif report_kind == "equipment":
        story.append(Paragraph(escape(labels["equipment_overview"]), styles["Heading2"]))
        for department in df["Abteilung"].drop_duplicates():
            story.extend(
                [
                    Spacer(1, 8),
                    Paragraph(escape(str(department)), styles["Heading3"]),
                ]
            )
            append_equipment_table(df[df["Abteilung"] == department])
    elif report_kind == "power":
        story.extend(
            [
                Paragraph(escape(labels["balancing"]), styles["Heading2"]),
                _table(
                    [
                        [labels["phase_assignment"], labels["active_power"], labels["current_230"]],
                        *[
                            [
                                phase,
                                f"{phase_watts[phase] / 1000:.2f} kW",
                                f"{phase_watts[phase] / 230:.2f} A",
                            ]
                            for phase in ("L1", "L2", "L3")
                        ],
                    ],
                    [150, 180, 180],
                ),
                Spacer(1, 14),
                Paragraph(escape(labels["detailed_assignment"]), styles["Heading2"]),
            ]
        )
        for phase in ("L1", "L2", "L3"):
            story.append(Paragraph(escape(labels["phase_assignment"] + f" {phase}"), styles["Heading3"]))
            story.extend(_paragraph(item, styles) for item in phases[phase])
            story.append(Spacer(1, 8))
    elif report_kind == "department":
        story.extend(
            [
                Paragraph(escape(labels["load_summary"]), styles["Heading2"]),
                Spacer(1, 8),
            ]
        )
        append_department_table()

    document.build(story)
    buffer.seek(0)
    return buffer, file_suffix
