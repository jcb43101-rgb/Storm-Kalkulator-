import streamlit as st

######## De Page Imports

from Pages.De.Calc_Page_De import Calc_Page_View_De
from Pages.De.Help_Page_De import Help_Page_View_De

#########   En Page Imports

from Pages.En.Help_Page_En import Help_Page_View_En
from Pages.En.Calc_Page_En import Calc_Page_View_En
########## App Function

def run_calc_page_de():
    Calc_Page_View_De(help_page_de, calc_page_de, calc_page_en)

def run_help_page_de():
    Help_Page_View_De (calc_page_de, help_page_de, help_page_en)

def run_calc_page_en():
    Calc_Page_View_En (help_page_en, calc_page_de, calc_page_en)

def run_help_page_en():
    Help_Page_View_En(calc_page_en, help_page_de, help_page_en)


# Set page config at the entrypoint

st.set_page_config(page_title="Filmlicht & Stromrechner", layout="wide")

# --- Page Definitions ---

# --- Page Routing Setup ---
calc_page_de = st.Page(run_calc_page_de, title="Stromrechner", icon="⚡", default=True)
help_page_de = st.Page(run_help_page_de, title="Hilfe", icon="❓")
calc_page_en = st.Page(run_calc_page_en, title="Power Calculator", icon="⚡")
help_page_en = st.Page(run_help_page_en, title="Help", icon="❓")

# Set position="hidden" to completely remove the sidebar navigation UI
pg = st.navigation(
    [calc_page_de, help_page_de, calc_page_en, help_page_en],
    position="hidden",
)
pg.run()