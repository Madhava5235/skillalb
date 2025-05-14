import streamlit as st
import requests
import json

# Amas AI (Groq) API Configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Function to query Amas AI API
def query_amas_ai(user_prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful and creative assistant."},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠ API Error: {response.text}"

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Page styling and config
st.set_page_config(page_title="Amas AI Chat", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .big-font {
        font-size: 30px !important;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }
    .chat-bubble {
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        max-width: 90%;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #DCF8C6;
        text-align: right;
    }
    .ai-msg {
        background-color: #F1F0F0;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-font">💬 Ask Amas AI Anything!</div>', unsafe_allow_html=True)
st.markdown("#### Powered by LLaMA 3 on Amas AI")

# Input prompt
user_input = st.text_area("📌 Enter your prompt:", height=150, placeholder="e.g., Suggest a creative reuse for broken bricks...")

# Generate response
if st.button("🚀 Generate Response") and user_input.strip():
    with st.spinner("Thinking... 🤖"):
        response = query_amas_ai(user_input)

    # Save the conversation to session state
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("ai", response))

# Display the chat history
if st.session_state.chat_history:
    st.markdown("### 🧾 Chat History:")
    for sender, msg in st.session_state.chat_history:
        css_class = "user-msg" if sender == "user" else "ai-msg"
        name = "You" if sender == "user" else "Amas AI"
        st.markdown(f"<div class='chat-bubble {css_class}'><strong>{name}:</strong><br>{msg}</div>", unsafe_allow_html=True)
