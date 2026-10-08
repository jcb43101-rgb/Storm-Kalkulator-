import math
from pathlib import Path
import pandas as pd
import streamlit as st
from Utilities.pdf_helpers import generate_pdf_report_De
from Utilities.pdf_helpers import generate_pdf_report_En
from Utilities.calculator_de import main_calculator_de
from Pages.De.Help_Page_De import help_page_de_view

# Set page config at the entrypoint
st.set_page_config(page_title="Filmlicht & Stromrechner", layout="wide")

# --- Page Definitions ---

# --- Page Routing Setup ---
calc_page_de = st.Page(main_calculator_de, title="Stromrechner", icon="⚡", default=True)
help_page_de = st.Page(help_page_de_view, title="Hilfe", icon="❓")

# Set position="hidden" to completely remove the sidebar navigation UI
pg = st.navigation([calc_page_de, help_page_de], position="hidden")
pg.run()