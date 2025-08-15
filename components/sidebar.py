import streamlit as st
from config.pages import PAGES

from utils.i18n import get_translations, LANGUAGES

def show_sidebar():
    """Display the navigation sidebar with authentication check."""
    # Setup translation
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'
    lang_display = {v: k for k, v in LANGUAGES.items()}
    current_language = st.session_state['language']
    t = get_translations()

    # Hide default Streamlit navigation
    st.markdown('''
        <style>
            /* Remove Streamlit sidebar default padding/margin */
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            /* Sidebar container */
            
            /* Sidebar title */
            .sidebar-content .sidebar-title {
                color: #2e2e2e !important;
                font-size: 1.2em;
                font-weight: 600;
                margin-bottom: 2rem;
                margin-top: 0.5rem;
                text-align: center;
                padding-bottom: 1rem;
                border-bottom: 1px solid #e0e0e0;
            }
            .sidebar-nav {
                display: flex;
                flex-direction: column;
                gap: 0.6rem;
                margin-bottom: 2rem;
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
                transition: background 0.2s, color 0.2s;
            }
            .nav-button:hover,
            .nav-button.active {
                background: #e0e0e0;
                color: #222;
            }
            .sidebar-divider {
                margin: 2rem 0 1rem 0;
                border-top: 1px solid #e0e0e0;
            }
            /* Dark theme override */
            @media (prefers-color-scheme: dark) {
                .sidebar-content {
                    background: #23272c !important;
                    color: #f6f6f6 !important;
                }
                /* Sidebar container */
                
                /* Sidebar title */
                .sidebar-content .sidebar-title {
                    color: #2e2e2e !important;
                    font-size: 1.2em;
                    font-weight: 600;
                    margin-bottom: 2rem;
                    margin-top: 0.5rem;
                    text-align: center;
                    padding-bottom: 1rem;
                    border-bottom: 1px solid #e0e0e0;
                }
                .sidebar-nav {
                    display: flex;
                    flex-direction: column;
                    gap: 0.6rem;
                    margin-bottom: 2rem;
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
                    transition: background 0.2s, color 0.2s;
                }
                .nav-button:hover,
                .nav-button.active {
                    background: #e0e0e0;
                    color: #222;
                }
                .sidebar-divider {
                    margin: 2rem 0 1rem 0;
                    border-top: 1px solid #e0e0e0;
                }
                /* Dark theme override */
                @media (prefers-color-scheme: dark) {
                    .sidebar-content {
                        background: #23272c !important;
                        color: #f6f6f6 !important;
                    }
                    .sidebar-content .sidebar-title {
                        color: #f6f6f6 !important;
                        border-bottom: 1px solid #3d4144;
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
                        border-top: 1px solid #3d4144;
                    }
                }
            </style>
        ''', unsafe_allow_html=True)
        
        # Sidebar content structure
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.markdown(f'<div class="sidebar-title">{t["title"]}</div>', unsafe_allow_html=True)

    # Navigation
    st.sidebar.markdown('<div class="sidebar-nav">', unsafe_allow_html=True)
    # Sidebar navigation logic
    if not st.session_state.get('authenticated', False):
        # Only show Home in sidebar for unauthenticated users
        if st.sidebar.button(f"🏠 {t['home']}", key="nav_home", use_container_width=True):
            st.switch_page("Home.py")
    else:
        page_trans = {
            'Home': t['home'],
            'Calculator': t['calculator'],
            'Truck Tracker': t['truck_tracker'],
            'History': t['history'],
            'AI Assistant': t['ai_assistant'],
            'Settings': t['settings']
        }
        for page_name, page_path in PAGES.items():
            icon = {
                'Home': '🏠',
                'Calculator': '📊',
                'Truck Tracker': '🚛',
                'History': '📈',
                'AI Assistant': '🤖',
                'Settings': '⚙️'
            }.get(page_name, '')
            display_name = page_trans.get(page_name, page_name)
            if st.sidebar.button(f"{icon} {display_name}", key=f"nav_{page_name}", use_container_width=True):
                st.switch_page(f"{page_path}.py")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)  # close sidebar-nav

    # Language selection (moved to bottom, above copyright)
    selected_lang = st.sidebar.selectbox(
        t['language'],
        options=list(LANGUAGES.keys()),
        index=list(LANGUAGES.values()).index(current_language)
    )
    new_language = LANGUAGES[selected_lang]
    if new_language != current_language:
        st.session_state['language'] = new_language
        st.rerun()

    # Footer
    st.sidebar.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        f'<div style="color: #6b7280; font-size: 0.8em; text-align: center; padding: 1rem 0;">'
        f' {t["footer"]}<a href="https://welink-tech.tn/" target="_blank">Welink Tech</a>.</div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown('</div>', unsafe_allow_html=True)  # close sidebar-content