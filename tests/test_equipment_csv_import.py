import unittest

from Utilities.Equipment_CSV_Import import parse_equipment_csv
from Utilities.Translations import PAGE_TEXT


class EquipmentCsvImportTests(unittest.TestCase):
    def test_imports_app_export_csv_and_maps_departments_to_current_language(self):
        content = (
            "Gerätename,Abteilung,Anzahl,Leistung_W,Power_Factor,Spannung_V\n"
            "Key light,Lighting,2,650,0.95,230\n"
        ).encode("utf-8")

        equipment = parse_equipment_csv(
            content,
            locale="fr",
            departments=PAGE_TEXT["fr"]["departments"],
        )

        self.assertEqual(
            ["Gerätename", "Abteilung", "Anzahl", "Leistung_W", "Power_Factor", "Spannung_V"],
            list(equipment.columns),
        )
        self.assertEqual("Éclairage", equipment.loc[0, "Abteilung"])
        self.assertEqual(2, equipment.loc[0, "Anzahl"])
        self.assertEqual(230, equipment.loc[0, "Spannung_V"])

    def test_imports_semicolon_csv_with_localized_column_names(self):
        content = (
            "Nom de l’équipement;Département;Quantité;Puissance (W);"
            "Facteur de puissance;Tension (V)\n"
            "Projecteur;Éclairage;1;500;0.9;230\n"
        ).encode("utf-8-sig")

        equipment = parse_equipment_csv(
            content,
            locale="en",
            departments=["Lighting", "Sound", "Camera / Video", "Production", "Catering"],
        )

        self.assertEqual("Lighting", equipment.loc[0, "Abteilung"])
        self.assertEqual(500, equipment.loc[0, "Leistung_W"])

    def test_rejects_out_of_range_values_and_reports_csv_row(self):
        content = (
            "Gerätename,Abteilung,Anzahl,Leistung_W,Power_Factor,Spannung_V\n"
            "Key light,Lighting,1,650,1.2,230\n"
        ).encode("utf-8")

        with self.assertRaisesRegex(ValueError, "Power factor.*row\\(s\\): 2"):
            parse_equipment_csv(
                content,
                locale="en",
                departments=[
                    "Lighting",
                    "Sound",
                    "Camera / Video",
                    "Production",
                    "Catering",
                ],
            )

    def test_rejects_missing_required_columns(self):
        content = b"Geratename,Leistung_W\nKey light,650\n"

        with self.assertRaisesRegex(ValueError, "Missing required CSV columns"):
            parse_equipment_csv(
                content,
                locale="en",
                departments=[
                    "Lighting",
                    "Sound",
                    "Camera / Video",
                    "Production",
                    "Catering",
                ],
            )


if __name__ == "__main__":
    unittest.main()
