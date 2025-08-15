import streamlit as st
from config.pages import PAGES
from utils.i18n import get_translations, LANGUAGES

def show_sidebar():
    """Display the navigation sidebar with authentication check."""
    # Setup translation
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'
    current_language = st.session_state['language']
    t = get_translations()

    # Add custom CSS for the sidebar
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                background: #f8f9fa;
                transition: all 0.3s ease;
            }
            .sidebar-title {
                color: #2e2e2e !important;
                font-size: 1.2em;
                font-weight: 600;
                margin: 0 0 2rem 0;
                text-align: center;
                padding: 0 0 1rem 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .sidebar-divider {
                margin: 1.5rem 0;
                border-top: 1px solid #e0e0e0;
            }
            .sidebar-nav {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
                margin: 0 0 1rem 0;
                padding: 0;
            }
            .nav-button {
                background: none;
                color: #222;
                border: none;
                border-radius: 8px;
                padding: 0.7rem 1rem;
                text-align: left;
                font-size: 1em;
                cursor: pointer;
                transition: all 0.2s ease;
                width: 100%;
                margin: 0;
            }
            .nav-button:hover,
            .nav-button.active {
                background: #e9ecef;
                color: #000;
            }
            .stSelectbox > div {
                margin-bottom: 1rem;
            }
            @media (prefers-color-scheme: dark) {
                [data-testid="stSidebar"] {
                    background: #23272c !important;
                    color: #f6f6f6 !important;
                }
                .sidebar-title {
                    color: #f6f6f6 !important;
                    border-bottom-color: #3d4144;
                }
                .nav-button {
                    color: #f6f6f6;
                }
                .nav-button:hover,
                .nav-button.active {
                    background: #3d4144;
                    color: #ffffff;
                }
                .sidebar-divider {
                    border-top-color: #3d4144;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar title
    st.sidebar.markdown(f'<div class="sidebar-title">{t["title"]}</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    page_trans = {
        'Home': t['home'],
        'Calculator': t['calculator'],
        'Truck Tracker': t['truck_tracker'],
        'History': t['history'],
        'AI Assistant': t['ai_assistant'],
        'Settings': t['settings']
    }
    
    page_icons = {
        'Home': '🏠',
        'Calculator': '📊',
        'Truck Tracker': '🚛',
        'History': '📈',
        'AI Assistant': '🤖',
        'Settings': '⚙️'
    }
    
    # Navigation buttons
    for page_name, page_path in PAGES.items():
        icon = page_icons.get(page_name, '')
        display_name = page_trans.get(page_name, page_name)
        
        if page_name == 'Home':
            if st.sidebar.button(f"{icon} {display_name}", key=f"nav_{page_name}", use_container_width=True):
                st.switch_page("streamlit_app.py")
        else:
            if st.sidebar.button(f"{icon} {display_name}", key=f"nav_{page_name}", use_container_width=True):
                st.switch_page(f"{page_path}.py")
    
    # Language selection
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    # Add language selection
    lang_options = list(LANGUAGES.keys())
    current_lang_name = [k for k, v in LANGUAGES.items() if v == current_language][0]
    selected_lang = st.sidebar.selectbox(
        t['language'],
        options=lang_options,
        index=lang_options.index(current_lang_name)
    )
    
    new_language = LANGUAGES[selected_lang]
    if new_language != current_language:
        st.session_state['language'] = new_language
        st.rerun()
    
    # Footer
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<div style="color: #6b7280; font-size: 0.8em; text-align: center; padding: 1rem 0;">'
        f' {t["footer"]} <a href="https://welink-tech.tn/" target="_blank">Welink Tech</a>.</div>',
        unsafe_allow_html=True
    )
