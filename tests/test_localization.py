import unittest

import pandas as pd

from Utilities.Master_Calc import (
    REPORT_LABELS_BY_LANGUAGE,
    UI_TEXT,
)
from Utilities.PDF_Translations import PDF_REPORT_LABELS
from Utilities.Translations import LOCALE_NAMES, PAGE_TEXT
from Utilities.pdf_helpers import generate_pdf_report, get_pdf_font_family


class LocalizationTests(unittest.TestCase):
    def test_all_locales_have_complete_page_and_calculator_text(self):
        locales = set(LOCALE_NAMES)
        expected_ui_keys = set(UI_TEXT["en"])
        expected_page_keys = set(PAGE_TEXT["hi"])

        self.assertEqual(locales, set(UI_TEXT))
        self.assertEqual(locales, set(REPORT_LABELS_BY_LANGUAGE))
        self.assertEqual(locales - {"de", "en"}, set(PDF_REPORT_LABELS))
        self.assertEqual(locales - {"de", "en"}, set(PAGE_TEXT))

        for locale in locales - {"de", "en"}:
            with self.subTest(locale=locale):
                self.assertEqual(expected_ui_keys, set(UI_TEXT[locale]))
                self.assertEqual(expected_page_keys, set(PAGE_TEXT[locale]))
                self.assertEqual(5, len(PAGE_TEXT[locale]["departments"]))
                self.assertEqual(5, len(PAGE_TEXT[locale]["sample_equipment"]))

    def test_localized_pdf_reports_embed_their_unicode_font(self):
        equipment = pd.DataFrame(
            [
                {
                    "Gerätename": "Sample light",
                    "Abteilung": "Lighting",
                    "Anzahl": 1,
                    "Leistung_W": 420,
                    "Spannung_V": 230,
                    "Gesamt_W": 420,
                    "Strom_Amps": 1.84,
                }
            ]
        )
        department_summary = pd.DataFrame(
            [
                {
                    "Abteilung": "Lighting",
                    "Gesamt_kW": 0.42,
                    "Gesamt_Amps_230V": 1.83,
                    "Apparent_kVA": 0.42,
                }
            ]
        )

        for locale, labels in PDF_REPORT_LABELS.items():
            with self.subTest(locale=locale):
                regular_font, bold_font = get_pdf_font_family(locale)
                report_type = next(iter(labels["report_types"]))
                report, _ = generate_pdf_report(
                    pdf_type=report_type,
                    project_name="Production",
                    director="Director",
                    gaffer="Gaffer",
                    df=equipment,
                    dept_summary=department_summary,
                    total_kw=0.42,
                    total_amps_230v=1.83,
                    total_kva=0.42,
                    min_gen_kva=0.53,
                    suggested_gen_kva=3,
                    phase_watts={"L1": 420, "L2": 0, "L3": 0},
                    phases={"L1": ["Sample light"], "L2": [], "L3": []},
                    labels=labels,
                    regular_font=regular_font,
                    bold_font=bold_font,
                )

                pdf_bytes = report.getvalue()
                self.assertGreater(len(pdf_bytes), 1000)
                self.assertIn(regular_font.encode("ascii"), pdf_bytes)


if __name__ == "__main__":
    unittest.main()
