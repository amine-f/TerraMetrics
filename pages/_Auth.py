import streamlit as st
from utils.page_config import set_page_config
from utils.i18n import get_translations
from auth.email_auth import register_user, login_user

set_page_config("Auth")
from components.sidebar import show_sidebar

t = get_translations()

def show_auth_page():
    """Display the authentication page with login and registration forms."""
    # Show custom sidebar
    show_sidebar()

    st.title("🔐 " + t.get("login_register", "Login / Register"))
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs([t.get("login", "Login"), t.get("register", "Register")])
    
    with tab1:  # Login tab
        with st.form("login_form"):
            email = st.text_input(t.get("email", "Email"))
            password = st.text_input(t.get("password", "Password"), type="password")
            submit = st.form_submit_button(t.get("login_button", "Login"))
            
            if submit:
                try:
                    user = login_user(email, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_id = user.id
                        st.session_state.current_page = "calculator"
                        st.rerun()
                except Exception as e:
                    st.error(t.get("error_during_login", "Error during login:") + f" {str(e)}")
    
    with tab2:  # Registration tab
        with st.form("registration_form"):
            email = st.text_input(t.get("email", "Email"))
            password = st.text_input(t.get("password", "Password"), type="password")
            confirm_password = st.text_input(t.get("confirm_password", "Confirm Password"), type="password")
            submit = st.form_submit_button(t.get("register_button", "Register"))
            
            if submit:
                if password != confirm_password:
                    st.error(t.get("passwords_do_not_match", "Passwords do not match!"))
                else:
                    try:
                        user = register_user(email, password)
                        if user:
                            st.success(t.get("registration_success", "Registration successful! Please login."))
                    except Exception as e:
                        st.error(t.get("error_during_registration", "Error during registration:") + f" {str(e)}")
