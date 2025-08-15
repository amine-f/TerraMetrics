import streamlit as st
from components.sidebar import show_sidebar

# Set page config first
st.set_page_config(
    page_title="Terrametrics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show the sidebar first
show_sidebar()

# Then import and run the main app
import Home

# Run the main app content
if __name__ == "__main__":
    Home.main_content()
