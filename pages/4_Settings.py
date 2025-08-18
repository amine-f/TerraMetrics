import streamlit as st
from utils.page_config import set_page_config
from utils.i18n import get_translations

t = get_translations()
set_page_config(t.get("settings", "Settings"))

from components.sidebar import show_sidebar
from components.ai_chat import floating_chat

# ... (rest of your page code)

# Hide default sidebar navigation
st.markdown('''
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
    </style>
''', unsafe_allow_html=True)

# Show custom sidebar
show_sidebar()

# Check authentication
if not st.session_state.get('authenticated', False):
    st.switch_page("Home.py")

st.title("⚙️ " + t.get("settings", "Settings"))

# Profile settings
st.subheader("👤 " + t.get("profile", "Profile"))
email = st.text_input(t.get("email", "Email"), value=st.session_state.user_email, disabled=True)
st.button(t.get("change_password", "Change Password"))

# Preferences
st.subheader("🎨 " + t.get("preferences", "Preferences"))
st.checkbox(t.get("dark_mode", "Dark Mode"), value=True)
st.checkbox(t.get("show_tips", "Show Tips"), value=True)
st.selectbox(t.get("default_view", "Default View"), [t.get("calculator", "Calculator"), t.get("history", "History")])

# Data Management
st.subheader("💾 " + t.get("data_management", "Data Management"))
if st.button(t.get("export_data", "Export Data")):
    st.info(t.get("coming_soon", "Coming soon!"))
if st.button(t.get("delete_account", "Delete Account")):
    st.warning(t.get("action_cannot_be_undone", "This action cannot be undone!"))
    if st.checkbox(t.get("i_understand_consequences", "I understand the consequences")):
        st.error(t.get("account_deletion_coming_soon", "Account deletion coming soon!"))
