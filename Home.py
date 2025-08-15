import streamlit as st
from utils.i18n import get_translations
from components.profile_menu import show_profile_menu
from components.sidebar import show_sidebar

def show_content():
    t = get_translations()
    # Show sidebar navigation
    show_sidebar()
    
    # Show profile menu only if authenticated
    if st.session_state.get('authenticated', False):
        show_profile_menu()
    
    # Main content
    st.title("🌍 " + t.get("title", "Terrametrics"))
    
    if not st.session_state.get('authenticated', False):
        # Show welcome message and auth page
        st.write(t.get("welcome_home", 
            "Welcome to Terrametrics! This tool helps you track and understand your carbon emissions.\n\n"
            "Features:\n"
            "- 🔑 User authentication to save your data\n"
            "- 🌍 Calculate your carbon footprint from various sources\n"
            "- 📊 View your historical data and trends\n"
            "- 📈 Beautiful visualizations of your impact\n\n"
            "Please log in or register below to get started!"
        ))
        
        # Create tabs for login and registration
        tab1, tab2 = st.tabs([t.get("login", "Login"), t.get("register", "Register")])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input(t.get("email", "Email"), key="login_email")
                password = st.text_input(t.get("password", "Password"), type="password", key="login_password")
                login_button = st.form_submit_button(t.get("login", "Login"))
                
                if login_button:
                    if email and password:
                        # Here you would validate credentials against your database
                        # For now, we'll just set authenticated to True
                        st.session_state.authenticated = True
                        st.session_state.email = email
                        st.rerun()
                    else:
                        st.error(t.get("login_error", "Please enter both email and password"))
        
        with tab2:
            with st.form("register_form"):
                st.write(t.get("register_prompt", "Create a new account"))
                new_email = st.text_input(t.get("email", "Email"), key="register_email")
                new_password = st.text_input(t.get("password", "Password"), 
                                          type="password", key="register_password1")
                confirm_password = st.text_input(t.get("confirm_password", "Confirm Password"), 
                                              type="password", key="register_password2")
                register_button = st.form_submit_button(t.get("register", "Register"))
                
                if register_button:
                    if new_password == confirm_password and new_email:
                        # Here you would save the new user to your database
                        st.success(t.get("register_success", "Registration successful! Please log in."))
                    else:
                        st.error(t.get("register_error", "Please check your details and try again"))
    else:
        # Show dashboard for authenticated users
        st.write(t.get("welcome_back", f"Welcome back, {st.session_state.get('email', 'User')}!"))
        # Add your dashboard content here

def main():
    """Main application entry point."""
    show_content()

if __name__ == "__main__":
    # Ensure all session state variables are initialized
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'email' not in st.session_state:
        st.session_state.email = ''
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'Home'
        
    main()
