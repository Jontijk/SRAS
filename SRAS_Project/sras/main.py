import sys
import os
import streamlit as st

# Add the parent directory of sras to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set Streamlit page config
st.set_page_config(
    page_title="Smart Research Assistant Suite (SRAS)",
    page_icon="🧠",
    layout="wide"
)

# Securely load Hugging Face token from Streamlit secrets
hf_token = st.secrets.get("sras-api")
if not hf_token:
    st.error("❌ Hugging Face token not found in Streamlit secrets.")
    st.stop()
else:
    os.environ["sras-api"] = hf_token

# Import UI modules
from sras.ui.summarizer_ui import summarize_ui
from sras.ui.finance_ui import finance_ui
from sras.ui.presentation_ui import presentation_ui
from sras.ui.calculation_ui import calculation_ui

# Sidebar for tool selection
st.sidebar.title("🧰 SRAS Tools")
tool = st.sidebar.radio("Choose a tool:", [
    "📝 Summarizer",
    "📊 Finance Agent",
    "📽️ Presentation Generator",
    "🔢 Calculation Agent"
])

# Main Title
st.title("🧠 Smart Research Assistant Suite (SRAS)")
st.markdown("Welcome! Select a tool from the sidebar to begin.")

# Tool router
if tool == "📝 Summarizer":
    summarize_ui()

elif tool == "📊 Finance Agent":
    finance_ui()

elif tool == "📽️ Presentation Generator":
    presentation_ui()

elif tool == "🔢 Calculation Agent":
    calculation_ui()
