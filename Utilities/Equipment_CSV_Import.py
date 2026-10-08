import csv
import hashlib
import io
import math
import re
import unicodedata

import pandas as pd
import streamlit as st

from Utilities.Translations import LOCALE_NAMES, PAGE_TEXT

EQUIPMENT_COLUMNS = (
    "Gerätename",
    "Abteilung",
    "Anzahl",
    "Leistung_W",
    "Power_Factor",
    "Spannung_V",
)

CSV_IMPORT_TEXT = {
    "de": {
        "label": "Geräteliste aus CSV importieren",
        "help": "Lädt die bestehende Liste mit dieser CSV hoch und ersetzt sie. Erforderliche Spalten: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "{count} Geräte aus der CSV importiert.",
    },
    "en": {
        "label": "Import equipment list from CSV",
        "help": "Upload a CSV to replace the current equipment list. Required columns: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Imported {count} devices from the CSV.",
    },
    "hi": {
        "label": "CSV से उपकरण सूची आयात करें",
        "help": "CSV अपलोड करने से मौजूदा उपकरण सूची बदल जाएगी। आवश्यक कॉलम: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V।",
        "success": "CSV से {count} उपकरण आयात किए गए।",
    },
    "pl": {
        "label": "Importuj listę sprzętu z CSV",
        "help": "Przesłanie CSV zastąpi bieżącą listę sprzętu. Wymagane kolumny: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Zaimportowano {count} urządzeń z CSV.",
    },
    "de_ch": {
        "label": "Geräteliste aus CSV importieren",
        "help": "Der CSV-Import ersetzt die aktuelle Geräteliste. Erforderliche Spalten: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "{count} Geräte aus der CSV importiert.",
    },
    "fr": {
        "label": "Importer la liste du matériel depuis un CSV",
        "help": "L’importation du CSV remplace la liste actuelle. Colonnes requises : Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "{count} appareils importés depuis le CSV.",
    },
    "ru": {
        "label": "Импортировать список оборудования из CSV",
        "help": "Импорт CSV заменит текущий список. Обязательные столбцы: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Импортировано устройств из CSV: {count}.",
    },
    "es": {
        "label": "Importar lista de equipos desde CSV",
        "help": "La importación del CSV reemplaza la lista actual. Columnas obligatorias: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Se importaron {count} equipos desde el CSV.",
    },
    "pt": {
        "label": "Importar lista de equipamentos de CSV",
        "help": "A importação do CSV substitui a lista atual. Colunas obrigatórias: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Foram importados {count} equipamentos do CSV.",
    },
    "it": {
        "label": "Importa elenco apparecchiature da CSV",
        "help": "L’importazione del CSV sostituisce l’elenco attuale. Colonne richieste: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "Importate {count} apparecchiature dal CSV.",
    },
    "ar": {
        "label": "استيراد قائمة المعدات من CSV",
        "help": "سيؤدي استيراد CSV إلى استبدال القائمة الحالية. الأعمدة المطلوبة: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "تم استيراد {count} من المعدات من ملف CSV.",
    },
    "he": {
        "label": "ייבוא רשימת ציוד מקובץ CSV",
        "help": "ייבוא CSV יחליף את הרשימה הנוכחית. העמודות הנדרשות: Gerätename, Abteilung, Anzahl, Leistung_W, Power_Factor, Spannung_V.",
        "success": "יובאו {count} פריטי ציוד מקובץ CSV.",
    },
}

_COLUMN_ALIASES = {
    "Gerätename": {
        "gerätename",
        "equipmentname",
        "devicename",
        "name",
        "nomdelequipement",
        "nombredelteam",
        "nomeequipamento",
        "nomeapparecchiatura",
        "اسمالمعدة",
        "שםהציוד",
    },
    "Abteilung": {
        "abteilung",
        "department",
        "dept",
        "departamento",
        "departement",
        "reparto",
        "قسم",
        "מחלקה",
    },
    "Anzahl": {
        "anzahl",
        "quantity",
        "qty",
        "cantidad",
        "quantidade",
        "quantità",
        "quantita",
        "quantité",
        "quantite",
    },
    "Leistung_W": {
        "leistungw",
        "leistungwatt",
        "powerw",
        "powerwatts",
        "watts",
        "watt",
        "power",
        "leistung",
        "potenciaw",
        "puissancew",
        "potenzaw",
        "potenzaw",
        "potencia",
        "potenza",
        "vermogenw",
        "potencjaw",
        "potencja",
        "القدرةw",
        "הספקw",
        "הספק",
    },
    "Power_Factor": {
        "powerfactor",
        "cosφ",
        "cosphi",
        "leistungsfaktor",
        "factordepotencia",
        "facteurdepuissance",
        "fatordepotencia",
        "faktormocy",
        "fattoredipotenza",
        "wspolczynnikmocy",
        "معاملالقدرة",
        "מקדםהספק",
    },
    "Spannung_V": {
        "spannungv",
        "voltagev",
        "voltage",
        "spannung",
        "tension",
        "tensionv",
        "tensão",
        "tensao",
        "tensaov",
        "tensione",
        "الجهد",
        "الجهدv",
        "מתח",
        "מתחv",
    },
}

_DEPARTMENTS_BY_LOCALE = {
    **{
        locale: tuple(PAGE_TEXT[locale]["departments"])
        for locale in PAGE_TEXT
    },
    "de": ("Licht", "Ton", "Kamera / Video", "Produktion", "Catering"),
    "en": ("Lighting", "Sound", "Camera / Video", "Production", "Catering"),
}


def _normalize_header(value: object) -> str:
    normalized = unicodedata.normalize("NFKD", str(value).casefold())
    normalized = "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )
    return re.sub(r"[\W_]+", "", normalized, flags=re.UNICODE)


def _normalize_department(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip().casefold())


_DEPARTMENT_INDEX = {
    _normalize_department(department): index
    for departments in _DEPARTMENTS_BY_LOCALE.values()
    for index, department in enumerate(departments)
}


def parse_equipment_csv(
    content: bytes, *, locale: str, departments: list[str]
) -> pd.DataFrame:
    if not content:
        raise ValueError("The CSV file is empty.")

    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("The CSV file must use UTF-8 encoding.") from exc

    try:
        dialect = csv.Sniffer().sniff(text[:8192], delimiters=",;\t")
        source = pd.read_csv(
            io.StringIO(text),
            sep=dialect.delimiter,
            decimal="," if dialect.delimiter in {";", "\t"} else ".",
        )
    except (
        csv.Error,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        UnicodeDecodeError,
        ValueError,
    ) as exc:
        raise ValueError("Could not read the CSV file. Check its delimiter and format.") from exc

    header_lookup: dict[str, str] = {}
    for column in source.columns:
        normalized = _normalize_header(column)
        match = next(
            (
                target
                for target, aliases in _COLUMN_ALIASES.items()
                if normalized in {_normalize_header(alias) for alias in aliases}
            ),
            None,
        )
        if match is not None:
            if match in header_lookup.values():
                raise ValueError(f"The CSV contains more than one column for {match}.")
            header_lookup[str(column)] = match

    missing = set(EQUIPMENT_COLUMNS) - set(header_lookup.values())
    if missing:
        raise ValueError(
            "Missing required CSV columns: " + ", ".join(sorted(missing)) + "."
        )

    source = source.rename(columns=header_lookup)[list(EQUIPMENT_COLUMNS)]
    source = source.dropna(how="all").reset_index(drop=True)
    if source.empty:
        raise ValueError("The CSV contains no equipment rows.")

    source["Gerätename"] = source["Gerätename"].astype("string").str.strip()
    invalid_names = source["Gerätename"].isna() | source["Gerätename"].eq("")
    if invalid_names.any():
        raise ValueError(
            "Equipment names are required. Check CSV row(s): "
            + _row_numbers(invalid_names)
            + "."
        )

    numeric_columns = ("Anzahl", "Leistung_W", "Power_Factor", "Spannung_V")
    for column in numeric_columns:
        source[column] = pd.to_numeric(source[column], errors="coerce")
        invalid = source[column].map(
            lambda value: pd.isna(value) or not math.isfinite(value)
        )
        if invalid.any():
            raise ValueError(
                f"{column} must contain numbers. Check CSV row(s): "
                + _row_numbers(invalid)
                + "."
            )

    invalid_quantity = (source["Anzahl"] < 1) | (
        source["Anzahl"] % 1 != 0
    )
    if invalid_quantity.any():
        raise ValueError(
            "Quantity must be a whole number greater than zero. Check CSV row(s): "
            + _row_numbers(invalid_quantity)
            + "."
        )

    invalid_power = source["Leistung_W"] <= 0
    if invalid_power.any():
        raise ValueError(
            "Power must be greater than zero watts. Check CSV row(s): "
            + _row_numbers(invalid_power)
            + "."
        )

    invalid_factor = (source["Power_Factor"] < 0.1) | (
        source["Power_Factor"] > 1
    )
    if invalid_factor.any():
        raise ValueError(
            "Power factor must be between 0.1 and 1.0. Check CSV row(s): "
            + _row_numbers(invalid_factor)
            + "."
        )

    invalid_voltage = ~source["Spannung_V"].isin((230, 400))
    if invalid_voltage.any():
        raise ValueError(
            "Voltage must be 230 or 400 V. Check CSV row(s): "
            + _row_numbers(invalid_voltage)
            + "."
        )

    department_indices = source["Abteilung"].map(
        lambda value: _DEPARTMENT_INDEX.get(_normalize_department(value))
    )
    if department_indices.isna().any():
        bad_values = sorted(
            {
                str(value)
                for value in source.loc[department_indices.isna(), "Abteilung"]
            }
        )
        raise ValueError(
            "Unrecognized department(s): "
            + ", ".join(bad_values)
            + ". Use a department name from the app's equipment list."
        )

    localized_departments = _DEPARTMENTS_BY_LOCALE.get(locale)
    if localized_departments is None:
        raise ValueError(f"Unsupported locale: {locale}.")
    source["Abteilung"] = department_indices.map(
        lambda index: localized_departments[int(index)]
    )
    if list(localized_departments) != list(departments):
        raise ValueError("The department list does not match the selected locale.")

    source["Anzahl"] = source["Anzahl"].astype(int)
    source["Spannung_V"] = source["Spannung_V"].astype(int)
    return source


def render_equipment_csv_import(
    default_data: pd.DataFrame,
    *,
    locale: str,
    departments: list[str],
    upload_label: str,
    help_text: str,
    success_text: str,
    editor_key: str,
    column_config: dict,
) -> pd.DataFrame:
    upload = st.file_uploader(
        upload_label,
        type=["csv"],
        help=help_text,
        key=f"equipment_csv_upload_{locale}",
    )
    if upload is not None:
        fingerprint = hashlib.sha256(upload.getvalue()).hexdigest()
        fingerprint_key = f"equipment_csv_fingerprint_{locale}"
        if st.session_state.get(fingerprint_key) != fingerprint:
            try:
                imported = parse_equipment_csv(
                    upload.getvalue(), locale=locale, departments=departments
                )
            except ValueError as exc:
                st.error(str(exc))
            else:
                st.session_state.pop(editor_key, None)
                st.session_state[fingerprint_key] = fingerprint
                default_data = imported
                st.success(success_text.format(count=len(imported)))

    return st.data_editor(
        default_data,
        num_rows="dynamic",
        column_config=column_config,
        key=editor_key,
        use_container_width=True,
    )


def _row_numbers(mask: pd.Series) -> str:
    return ", ".join(str(int(index) + 2) for index in mask[mask].index)
