import streamlit as st

# Initialize session states at the very top
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if not hasattr(st.session_state, 'email'):
    st.session_state.email = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "auth"

from utils.page_config import set_page_config
from utils.i18n import get_translations

# Set page config with favicon
set_page_config("Home")

# Import after st.set_page_config to avoid any potential conflicts
from components.profile_menu import show_profile_menu
from components.sidebar import show_sidebar
from config.pages import hide_pages
from auth.email_auth import register_user, login_user

# Hide pages when not authenticated
hide_pages()

def main_content():
    """Main application content without sidebar."""
    t = get_translations()
    
    # Show profile menu only if authenticated
    if st.session_state.authenticated:
        show_profile_menu()

    # Main content
    st.title("🌍 " + t.get("title", "Terrametrics"))
    
    if not st.session_state.authenticated:
        # Show welcome message and auth page
        st.write(t.get("welcome_home", "Welcome to Terrametrics! This tool helps you track and understand your carbon emissions.\n\nFeatures:\n- 🔑 User authentication to save your data\n- 🌍 Calculate your carbon footprint from various sources\n- 📊 View your historical data and trends\n- 📈 Beautiful visualizations of your impact\n\nPlease log in or register below to get started!"))
        
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
                            st.session_state.email = user['email']
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
    else:
        # Show welcome message for authenticated users
        st.write(t.get("welcome_back", f"Welcome back, {st.session_state.email}! 👋\n\nUse the sidebar to:\n- 🌍 Calculate your carbon footprint\n- 📊 View your emission history"))

def main():
    """Legacy main function for backward compatibility."""
    # This is kept for backward compatibility but will be removed in future
    main_content()

if __name__ == "__main__":
    main()
