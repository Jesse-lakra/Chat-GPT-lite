import streamlit as st
from openai import OpenAI

# ==============================
# Setup OpenAI Client
# ==============================

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================
# Simple Content Filter
# ==============================

banned_words = [
    "sex", "porn", "nude", "kill", "murder", "drugs",
    "hate", "terror", "bomb", "rape"
]

def is_safe(prompt):
    prompt = prompt.lower()
    for word in banned_words:
        if word in prompt:
            return False
    return True

# ==============================
# Streamlit UI
# ==============================

st.title("Mini SafeGPT 🤖")
st.write("This AI avoids unethical and vulgar responses.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask something:")

if st.button("Send"):

    if not user_input.strip():
        st.warning("Please enter a question.")
    
    elif not is_safe(user_input):
        st.error("This question violates safety guidelines.")
    
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. You must avoid unethical, illegal, harmful, or vulgar content. Keep answers professional and clean."
                    },
                    {"role": "user", "content": user_input}
                ]
            )

            answer = response.choices[0].message.content

            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("AI", answer))

        except Exception as e:
            st.error("API Error. Check your API key.")

# ==============================
# Display Chat History
# ==============================

for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")