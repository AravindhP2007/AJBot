import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configure Gemini API
genai.configure(api_key="AIzaSyAL2phbSkcnpSjh0eswgXp3k2N0rbNSAfU")  

model = genai.GenerativeModel("gemini-1.5-flash")

# Modify Gemini responses
def modify_response(response_text):
    replacements = {
        "I am a large language model, trained by Google.": "I am a large language model AJ Bot, trained by Aravindh & Jack Christopher",
        "I was created by Google.": "I was created by Aravindh & Jack Christopher.",
        "I don't have a name. I am a large language model, an AI.": "Myself AJ Bot. I am a large language model, an AI.",
        "I don't have a single creator. I was created by Google and am the result of years of research and development by many different people.  There's no single name associated with my creation.":
            "I don't have a single creator. I was created by Aravindh & Jack Christopher. There's no single name associated with my creation.",
        "I don't have a creator in the way a human artist or writer does. I was created by Google and am a large language model.  I don't have a single person or team who can be named as my creator because my development was a collaborative effort involving many researchers and engineers.":
            "I don't have a single creator. I was created by Aravindh & Jack Christopher. There's no single name associated with my creation.",
        "I don't have a creator in the same way a human artist or writer does.  I am a large language model, created by Google.":
            "I don't have a single creator. I was created by Aravindh & Jack Christopher. There's no single name associated with my creation.",
    }
    return replacements.get(response_text.strip(), response_text)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Page config
st.set_page_config(page_title="AJ Bot 💬", layout="centered")
st.title("💬 AJ Bot")

# --- Main UI ---

# Input Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type something...", key="user_input", label_visibility="collapsed", placeholder="Type something...", autocomplete="off")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    try:
        response = model.generate_content(user_input)
        reply = modify_response(response.text)

        # Save to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("AJ Bot", reply))

    except ResourceExhausted:
        st.session_state.chat_history.append(("AJ Bot", "Too many requests! Please wait a minute..."))

    # Refresh the app cleanly
    st.rerun()  # ✅ <-- New correct method (not experimental_rerun)

# Display chat history
for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**{speaker}:** {message}")
    else:
        st.markdown(f"**{speaker}:** {message}")
