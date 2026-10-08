import streamlit as st
from Utilities.calculator_de import main_calculator_de
from Pages.De.Help_Page_De import help_page_de_view


def run_calculator_page():
    main_calculator_de(help_page_de)


def run_help_page():
    help_page_de_view(calc_page_de)


# Set page config at the entrypoint
st.set_page_config(page_title="Filmlicht & Stromrechner", layout="wide")

# --- Page Definitions ---

# --- Page Routing Setup ---
calc_page_de = st.Page(run_calculator_page, title="Stromrechner", icon="⚡", default=True)
help_page_de = st.Page(run_help_page, title="Hilfe", icon="❓")

# Set position="hidden" to completely remove the sidebar navigation UI
pg = st.navigation([calc_page_de, help_page_de], position="hidden")
pg.run()