import streamlit as st

######## De Page Imports

from Pages.De.Calc_Page_De import Calc_Page_View_De
from Pages.De.Help_Page_De import Help_Page_View_De

#########   En Page Imports

from Pages.En.Help_Page_En import Help_Page_View_En
from Pages.En.Calc_Page_En import Calc_Page_View_En
from Pages.Localized_Pages import render_localized_calculator, render_localized_help
from Utilities.Translations import LOCALE_NAMES, PAGE_TEXT
########## App Function

def run_calc_page_de():
    Calc_Page_View_De(help_page_de, calc_page_de, calc_page_en, calculator_pages)

def run_help_page_de():
    Help_Page_View_De(calc_page_de, help_page_de, help_page_en, help_pages)

def run_calc_page_en():
    Calc_Page_View_En(help_page_en, calc_page_de, calc_page_en, calculator_pages)

def run_help_page_en():
    Help_Page_View_En(calc_page_en, help_page_de, help_page_en, help_pages)

def make_localized_calculator(locale):
    def run():
        render_localized_calculator(locale, calculator_pages, help_pages)
    return run

def make_localized_help(locale):
    def run():
        render_localized_help(locale, calculator_pages, help_pages)
    return run

# Set page config at the entrypoint

st.set_page_config(page_title="Filmlicht & Stromrechner", layout="wide")

# --- Page Definitions ---

# --- Page Routing Setup ---
calc_page_de = st.Page(run_calc_page_de, title="Stromrechner", icon="⚡", default=True)
help_page_de = st.Page(run_help_page_de, title="Hilfe", icon="❓")
calc_page_en = st.Page(run_calc_page_en, title="Power Calculator", icon="⚡")
help_page_en = st.Page(run_help_page_en, title="Help", icon="❓")

calculator_pages = {
    LOCALE_NAMES["de"]: calc_page_de,
    LOCALE_NAMES["en"]: calc_page_en,
}
help_pages = {
    LOCALE_NAMES["de"]: help_page_de,
    LOCALE_NAMES["en"]: help_page_en,
}

for locale in ("hi", "pl", "de_ch", "fr", "ru"):
    locale_name = LOCALE_NAMES[locale]
    calculator_pages[locale_name] = st.Page(
        make_localized_calculator(locale),
        title=PAGE_TEXT[locale]["calc_title"],
        icon="⚡",
        url_path=f"{locale}_calculator",
    )
    help_pages[locale_name] = st.Page(
        make_localized_help(locale),
        title=PAGE_TEXT[locale]["help_title"],
        icon="❓",
        url_path=f"{locale}_help",
    )

# Set position="hidden" to completely remove the sidebar navigation UI
pg = st.navigation(
    [*calculator_pages.values(), *help_pages.values()],
    position="hidden",
)
pg.run()
