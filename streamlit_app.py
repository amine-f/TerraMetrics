import streamlit as st
from components.sidebar import show_sidebar

# Show the sidebar first
show_sidebar()

# Then import and run the main app
import Home

# This file is needed for Streamlit Community Cloud deployment.
# It imports and runs the main function from your Home.py file.
if __name__ == "__main__":
    # Pass show_sidebar_nav=False to prevent duplicate sidebar
    Home.main(show_sidebar_nav=False)
