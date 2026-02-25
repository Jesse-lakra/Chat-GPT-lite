import streamlit as st
import requests

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(page_title="SafeGPT Free", page_icon="🤖")

st.title("🤖 SafeGPT - Free AI Assistant")
st.write("This AI avoids unethical, harmful, or vulgar responses.")

# =====================================
# LOAD HUGGING FACE TOKEN
# =====================================

if "HF_TOKEN" not in st.secrets:
    st.error("Hugging Face token not found.")
    st.info("Go to Manage App → Secrets and add:")
    st.code('HF_TOKEN = "your_token_here"')
    st.stop()

HF_TOKEN = st.secrets["HF_TOKEN"]

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# =====================================
# BASIC SAFETY FILTER
# =====================================

banned_words = [
    "sex", "porn", "nude", "rape", "kill", "murder",
    "drugs", "bomb", "terror", "hate"
]

def is_safe(text):
    text = text.lower()
    for word in banned_words:
        if word in text:
            return False
    return True

# =====================================
# CHAT MEMORY
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================
# MODEL QUERY FUNCTION
# =====================================

def query_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 503:
        return "Model is loading. Please wait 30 seconds and try again."
    elif response.status_code == 429:
        return "Rate limit exceeded. Please wait and try again."
    else:
        return f"Error: {response.status_code}"

# =====================================
# CHAT INPUT
# =====================================

user_input = st.chat_input("Ask something...")

if user_input:

    # Safety check
    if not is_safe(user_input):
        st.error("Your question violates safety guidelines.")
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        output = query_model(user_input)

        if isinstance(output, str):
            reply = output
        else:
            reply = output[0]["generated_text"]

        st.markdown(reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )