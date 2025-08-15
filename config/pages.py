import streamlit as st

PAGES = {
    "Home": "Home",
    "Calculator": "pages/2_Calculator",
    "Truck Tracker": "pages/5_Truck_Tracker",
    "History": "pages/3_History",
    "AI Assistant": "pages/6_AI_Chat",
    "Settings": "pages/4_Settings"
}

def hide_pages():
    """Hide pages from the sidebar when user is not authenticated."""
    # Hide all pages by default
    st.markdown('''
        <style>
            [data-testid="stSidebarNav"] {display: none !important;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    ''', unsafe_allow_html=True)
    
    # Show only Calculator and History pages when authenticated
    if st.session_state.get('authenticated', False):
        st.markdown('''
            <script>
                // Get all sidebar links
                var links = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] a');
                links.forEach(function(link) {
                    // Hide Home and Auth pages
                    if (link.textContent.includes('Home') || link.textContent.includes('Auth')) {
                        link.style.display = 'none';
                    }
                });
            </script>
        ''', unsafe_allow_html=True)
