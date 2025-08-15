import streamlit as st

def show_profile_menu():
    """Display the profile menu in the top right corner."""
    if st.session_state.authenticated:
        col1, col2 = st.columns([6, 1])
        with col2:
            with st.container(border=True):
                st.write(f"👤 {st.session_state.email}")
                if st.button("Logout", key="profile_logout"):
                    st.session_state.authenticated = False
                    st.session_state.email = None
                    st.rerun()
    else:
        col1, col2 = st.columns([6, 1])
        with col2:
            with st.container(border=True):
                st.write("👤 User")
                if st.button("Login", key="profile_login"):
                    st.session_state.current_page = "auth"
                    st.rerun()
