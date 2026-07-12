import streamlit as str
import google.generativeai as genai
import os

# Page configurations
str.set_page_config(page_title="Neshu AI", page_icon="🧠", layout="centered")

str.title("🧠 Neshu AI")
str.write("මගෙන් ඕනෑම දෙයක් අහන්න, මම හැමදේම දන්න Neshu AI කෙනෙක්!")

# Securely fetch API Key from Render environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    str.error("🚨 Configuration Error: Gemini API Key එක සෙට් කරලා නැහැ. Please add GEMINI_API_KEY to Render Environment Variables.")
else:
    # Configure Gemini API
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Initialize chat history in session state
    if "messages" not in str.session_state:
        str.session_state.messages = []

    # Display past chat messages
    for msg in str.session_state.messages:
        with str.chat_message(msg["role"]):
            str.markdown(msg["content"])

    # User input field
    if user_prompt := str.chat_input("Neshu AI ගෙන් මොනවද දැනගන්න ඕනේ?"):
        # Display user message
        with str.chat_message("user"):
            str.markdown(user_prompt)
        
        # Save to history
        str.session_state.messages.append({"role": "user", "content": user_prompt})

        # Generate response from AI
        with str.chat_message("assistant"):
            message_placeholder = str.empty()
            try:
                # Instructing the model to act specifically as Neshu AI
                full_prompt = f"You are Neshu AI, an omniscient, all-knowing smart AI assistant. Answer accurately as Neshu AI: {user_prompt}"
                response = model.generate_content(full_prompt)
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # Save AI response to history
                str.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                str.error(f"Error එකක් වුණා: {str(e)}")
