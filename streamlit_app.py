import streamlit as st

# Set page config first - this must be the first Streamlit command
st.set_page_config(
    page_title="Terrametrics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide the default Streamlit sidebar and adjust layout
st.markdown("""
    <style>
        /* Hide the default sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Style our custom sidebar */
        .custom-sidebar {
            position: fixed;
            left: 0;
            top: 0;
            width: 300px;
            height: 100vh;
            background: #f0f2f6;
            padding: 1rem;
            overflow-y: auto;
            z-index: 999;
        }
        
        /* Adjust main content area to account for sidebar */
        .main .block-container {
            margin-left: 300px !important;
            padding: 1rem 2rem;
            max-width: calc(100% - 300px) !important;
        }
        
        /* Ensure content is properly aligned */
        .stApp {
            padding-left: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'email' not in st.session_state:
    st.session_state.email = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "auth"

# Create our custom sidebar container
with st.sidebar:
    st.markdown('<div class="custom-sidebar">', unsafe_allow_html=True)
    from components.sidebar import show_sidebar
    show_sidebar()
    st.markdown('</div>', unsafe_allow_html=True)

# Import and run the main app content
import Home
Home.show_content()
