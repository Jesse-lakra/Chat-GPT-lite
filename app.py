import streamlit as st
import os
from openai import OpenAI

# ====================================
# PAGE CONFIG
# ====================================
st.set_page_config(page_title="SafeGPT", page_icon="🤖")

st.title("🤖 SafeGPT - Clean AI Assistant")
st.write("This AI avoids unethical, harmful, or vulgar responses.")

# ====================================
# GET API KEY SAFELY
# ====================================

api_key = None

# Try Streamlit secrets (Cloud)
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

# Try environment variable (Local)
elif os.getenv("OPENAI_API_KEY"):
    api_key = os.getenv("OPENAI_API_KEY")

# If key missing → stop app safely
if not api_key:
    st.error("OpenAI API key not found.")
    st.info("If using Streamlit Cloud → Go to Manage App → Secrets and add:")
    st.code('OPENAI_API_KEY = "your-key-here"')
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=api_key)

# ====================================
# BASIC SAFETY FILTER
# ====================================

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

# ====================================
# CHAT MEMORY
# ====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ====================================
# CHAT INPUT
# ====================================

user_input = st.chat_input("Ask something...")

if user_input:

    # Check safety
    if not is_safe(user_input):
        st.error("Your question violates safety guidelines.")
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional AI assistant. "
                                   "Avoid unethical, illegal, harmful, or vulgar content. "
                                   "Keep responses clean and respectful."
                    }
                ] + st.session_state.messages
            )

            reply = response.choices[0].message.content

            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as e:
            st.error("Error generating response. Check API key or billing.")