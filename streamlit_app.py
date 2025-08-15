import streamlit as st
from components.sidebar import show_sidebar

# Set page config first
st.set_page_config(
    page_title="Terrametrics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'email' not in st.session_state:
    st.session_state.email = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "auth"

# Show the sidebar
show_sidebar()

# Import and run the main app content
import Home
Home.show_content()
