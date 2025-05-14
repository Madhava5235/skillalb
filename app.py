import streamlit as st
import requests

# Amas AI (Groq) API Config
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Amas AI, a helpful and creative assistant."}
    ]

# Function to call Groq API with full chat history
def get_amas_response():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": GROQ_MODEL,
        "messages": st.session_state.messages
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"⚠ API Error: {response.text}"

# Streamlit UI config
st.set_page_config("Amas AI Chat", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
    .chat-container {
        margin-top: 20px;
        border-radius: 10px;
        padding: 15px;
        background-color: #f9f9f9;
    }
    .chat-bubble {
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        max-width: 95%;
        word-wrap: break-word;
    }
    .user-msg { background-color: #DCF8C6; text-align: right; }
    .ai-msg { background-color: #F1F0F0; text-align: left; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💬 Amas AI Chat")
st.caption("Built on LLaMA 3 via Groq API")

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[1:]:  # Skip system prompt
    role_class = "user-msg" if msg["role"] == "user" else "ai-msg"
    name = "You" if msg["role"] == "user" else "Amas AI"
    st.markdown(
        f"<div class='chat-bubble {role_class}'><strong>{name}:</strong><br>{msg['content']}</div>",
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# User input box
user_prompt = st.chat_input("Type your message here...")

# Process new input
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.spinner("Amas AI is thinking..."):
        ai_response = get_amas_response()
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.rerun()  # Refresh to display new message
