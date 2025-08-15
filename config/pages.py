import streamlit as st

# Define page paths relative to the root directory
PAGES = {
    "Home": "streamlit_app",  # Points to streamlit_app.py in root
    "Calculator": "pages/2_Calculator",
    "Truck Tracker": "pages/5_Truck_Tracker",
    "History": "pages/3_History",
    "AI Assistant": "pages/6_AI_Chat",
    "Settings": "pages/4_Settings"
}

def hide_pages():
    """Hide pages from the sidebar when user is not authenticated.
    
    This function hides the default Streamlit sidebar navigation and shows/hides
    pages based on authentication status.
    """
    # Initialize session state for authentication if not exists
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Hide all pages by default
    st.markdown('''
        <style>
            /* Hide default Streamlit sidebar navigation */
            [data-testid="stSidebarNav"] {display: none !important;}
            /* Hide Streamlit menu and footer */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    ''', unsafe_allow_html=True)
    
    # If authenticated, ensure certain pages are hidden
    if st.session_state.authenticated:
        st.markdown('''
            <script>
                // This script runs after the page loads to hide specific navigation items
                function hideNavigationItems() {
                    // Get all sidebar links
                    const links = window.parent.document.querySelectorAll('[data-testid="stSidebarNav"] a');
                    links.forEach(function(link) {
                        // Hide Auth pages if shown
                        if (link.textContent.includes('Auth')) {
                            link.style.display = 'none';
                        }
                    });
                }
                
                // Run on page load and after navigation
                hideNavigationItems();
                // Also run after a short delay to catch dynamically loaded elements
                setTimeout(hideNavigationItems, 1000);
            </script>
        ''', unsafe_allow_html=True)
