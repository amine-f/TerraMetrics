import streamlit as st
import requests
from streamlit_chat import message

# --- CONFIG ---
SYSTEM_PROMPT = (
    "You are Terrametrics AI, an assistant developed by Terrametrics. "
    "You help users with questions about clean energy, carbon dioxide emissions, and sustainability. "
    "Answer in a friendly, professional tone."
)

# --- API KEY ---
# Place your Mistral API key in .streamlit/secrets.toml as MISTRAL_API_KEY
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]  # Get your key at https://console.mistral.ai/api-keys

# Mistral API reference: https://docs.mistral.ai/api/


# --- CHATBOT LOGIC ---
def get_terrametrics_response(user_input, chat_history):
    # Mistral expects a list of message dicts with 'role' and 'content'.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_input})
    try:
        response = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistral-large-latest",  # You can change to another Mistral model if needed
                "messages": messages,
                "temperature": 0.3
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[Error communicating with Mistral API: {str(e)}]"

# --- CHAT UI ---
def floating_chat():
    # Only show if user is authenticated
    if not st.session_state.get('authenticated', False):
        return
    
    # Floating button CSS
    st.markdown('''
        <style>
        #terrametrics-float-chat {
            position: fixed;
            bottom: 32px;
            right: 32px;
            z-index: 9999;
        }
        #terrametrics-float-chat .stButton>button {
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 2rem;
            background: #26a69a;
            color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        #terrametrics-chatbox {
            position: fixed;
            bottom: 110px;
            right: 32px;
            width: 350px;
            max-width: 90vw;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.18);
            z-index: 10000;
            padding: 1.2rem 1rem 0.5rem 1rem;
            display: flex;
            flex-direction: column;
        }
        @media (prefers-color-scheme: dark) {
            #terrametrics-chatbox {
                background: #23272c;
                color: #f6f6f6;
            }
        }
        </style>
    ''', unsafe_allow_html=True)
    
    # Show/hide state
    if 'terrametrics_chat_open' not in st.session_state:
        st.session_state.terrametrics_chat_open = False
    
    # Floating chat button
    with st.container():
        st.markdown('<div id="terrametrics-float-chat">', unsafe_allow_html=True)
        if st.button("💬", key="terrametrics_float_btn"):
            st.session_state.terrametrics_chat_open = not st.session_state.terrametrics_chat_open
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chatbox
    if st.session_state.terrametrics_chat_open:
        st.markdown('<div id="terrametrics-chatbox">', unsafe_allow_html=True)
        st.markdown("<b>🤖 Terrametrics AI Assistant</b>", unsafe_allow_html=True)
        if "terrametrics_chat_history" not in st.session_state:
            st.session_state.terrametrics_chat_history = []
        for i, msg in enumerate(st.session_state.terrametrics_chat_history):
            message(msg["content"], is_user=(msg["role"] == "user"), key=f"{msg['role']}_{i}")
        user_input = st.text_input("Ask Terrametrics AI about clean energy or CO₂...", key="terrametrics_ai_input")
        if user_input:
            st.session_state.terrametrics_chat_history.append({"role": "user", "content": user_input})
            response = get_terrametrics_response(user_input, st.session_state.terrametrics_chat_history)
            st.session_state.terrametrics_chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
