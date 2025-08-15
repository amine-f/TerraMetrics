import streamlit as st
import base64
import os

def set_page_config(title):
    """Set page configuration including favicon"""
    # Path to favicon
    favicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', 'favicon.png')
    
    # Get favicon as base64 if it exists
    if os.path.exists(favicon_path):
        with open(favicon_path, "rb") as f:
            favicon_data = base64.b64encode(f.read()).decode()
        page_icon = f"data:image/png;base64,{favicon_data}"
    else:
        page_icon = "🌍"
    
    # Set page configurations (must be first Streamlit command)
    st.set_page_config(
        page_title=f"{title} | Terrametrics",
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
