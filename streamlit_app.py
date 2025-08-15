import streamlit as st

# Initialize all session state variables at the very beginning
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Only import Home after session state is initialized
import Home

# This file is needed for Streamlit Community Cloud deployment.
# It imports and runs the main function from your Home.py file.
if __name__ == "__main__":
    Home.main()
