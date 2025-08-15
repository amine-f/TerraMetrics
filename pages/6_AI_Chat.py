import streamlit as st
from utils.page_config import set_page_config
from utils.i18n import get_translations
from components.ai_chat import get_terrametrics_response
from components.sidebar import show_sidebar

t = get_translations()

set_page_config(t.get("ai_assistant", "AI Assistant"))
show_sidebar()

# Hide default Streamlit sidebar navigation
st.markdown('''
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
    </style>
''', unsafe_allow_html=True)


st.title("🤖 " + t.get("ai_assistant", "AI Assistant"))

if not st.session_state.get('authenticated', False):
    st.warning(t.get("please_login_first_ai", "Please login first to use the AI assistant."))
    st.stop()

st.markdown(t.get("assistant_description", """
This assistant developed by welink tech can answer your questions about clean energy, carbon dioxide emissions, and sustainability.
Ask anything and Terrametrics AI will help you!
"""))

if "terrametrics_chat_history" not in st.session_state:
    st.session_state.terrametrics_chat_history = []

for i, msg in enumerate(st.session_state.terrametrics_chat_history):
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = ""
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Use a unique key for the input to force clearing
if "input_key" not in st.session_state:
    st.session_state.input_key = 0
input_value = "" if st.session_state.clear_input else None
user_input = st.text_input(
    t.get("ask_ai_placeholder", "Ask Terrametrics AI Assistant about clean energy or CO₂..."),
    key=f"terrametrics_ai_input_page_{st.session_state.input_key}",
    value=input_value if input_value is not None else ""
)
if st.session_state.clear_input:
    st.session_state.clear_input = False
    st.session_state.input_key += 1

send_clicked = st.button("✨", key="send_button", help=t.get("send_message", "Send message"), use_container_width=False)

# Only process if Enter is pressed (user_input) or send button is clicked (send_clicked)
process_message = False
if user_input and user_input != st.session_state.last_user_input:
    process_message = True
if send_clicked and user_input:
    process_message = True

if st.session_state.clear_input:
    st.session_state.clear_input = False

if process_message:
    # Only process a new user message if it is different from the last
    if user_input and user_input != st.session_state.last_user_input:
        # Prevent duplicate user message entries
        if not (st.session_state.terrametrics_chat_history and st.session_state.terrametrics_chat_history[-1]["role"] == "user" and st.session_state.terrametrics_chat_history[-1]["content"] == user_input):
            st.session_state.terrametrics_chat_history.append({"role": "user", "content": user_input})
        response = get_terrametrics_response(user_input, st.session_state.terrametrics_chat_history)
        st.session_state.last_user_input = user_input
        # Handle Mistral errors gracefully
        if response.startswith("[Error communicating with Welink AI model:"):
            if "401" in response:
                st.warning(t.get("unauthorized_cpu_limit", "Unauthorized: The CPU temperature limit has been reached. Please try again later."))
            elif "400" in response:
                st.warning(t.get("bad_request_cpu_limit", "Bad request: The CPU temperature limit has been reached. Please try again later."))
            elif "429" in response:
                st.warning(t.get("too_many_requests_cpu_limit", "You have hit the CPU temperature limit. Please wait and try again later."))
            else:
                st.warning(response)
            # Remove the last user message to prevent repeated errors
            if st.session_state.terrametrics_chat_history and st.session_state.terrametrics_chat_history[-1]["role"] == "user":
                st.session_state.terrametrics_chat_history.pop()
        else:
            # Prevent duplicate assistant response entries
            if not (st.session_state.terrametrics_chat_history and st.session_state.terrametrics_chat_history[-1]["role"] == "assistant" and st.session_state.terrametrics_chat_history[-1]["content"] == response):
                st.session_state.terrametrics_chat_history.append({"role": "assistant", "content": response})
        # Now clear input and rerun for next message
        st.session_state.clear_input = True
        st.session_state.input_key += 1
        st.rerun()



