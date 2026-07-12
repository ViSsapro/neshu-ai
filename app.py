import streamlit as str
import google.generativeai as genai
import os
import uuid

# Page configurations
str.set_page_config(page_title="Neshu AI", page_icon="🧠", layout="centered")

# --- DARK MODE & STYLING CSS ---
str.markdown(
    """
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    div[data-testid="stChatMessage"] {
        background-color: #1E222B !important;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stChatInputContainer {
        background-color: #0E1117 !important;
    }
    h1, h2, h3, p, span, label {
        color: #FAFAFA !important;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1E222B;
        color: #FAFAFA;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #262730;
        z-index: 100;
    }
    .main .block-container {
        padding-bottom: 60px;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #181C24 !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p {
        color: #FAFAFA !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- INITIALIZE SESSION STATE FOR MULTIPLE CHATS ---
if "chats" not in str.session_state:
    # ළඟ තබා ගන්නා සියලුම චැට් ගබඩා කරන තැන
    str.session_state.chats = {}

if "current_chat_id" not in str.session_state:
    str.session_state.current_chat_id = None

# Function to start a brand new chat session
def start_new_chat():
    new_id = str(uuid.uuid4())
    str.session_state.chats[new_id] = {
        "title": "🆕 නව සංවාදය",
        "messages": []
    }
    str.session_state.current_chat_id = new_id

# If there are no chats at all, create the first one automatically
if not str.session_state.chats or str.session_state.current_chat_id is None:
    start_new_chat()

current_id = str.session_state.current_chat_id

# --- SIDEBAR MENU SYSTEM (වම් පැත්තේ මෙනු එක) ---
# Streamlit වල Sidebar එකක් හැදුවාම ඉබේම වම් පැත්තේ උඩින් ඉරි කෑලි තුනේ (Hamburger) බටන් එක හැදෙනවා.
with str.sidebar:
    str.markdown("# 🧠 Neshu AI")
    str.markdown("---")
    
    # New Chat Button
    if str.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        str.rerun()
        
    str.markdown("---")
    
    # Total Chat Count Display
    total_chats = len(str.session_state.chats)
    str.write(f"📊 **ඔබගේ සමස්ත චැට් ගණන:** {total_chats}")
    
    str.markdown("### 💬 CHAT LIST")
    
    # Displaying All Past Chats as individual clickable buttons
    for chat_id, chat_data in list(str.session_state.chats.items()):
        # Highlight active chat
        button_label = f"💬 {chat_data['title']}"
        if chat_id == current_id:
            button_label = f"▶️ {chat_data['title']} (Active)"
            
        if str.button(button_label, key=chat_id, use_container_width=True):
            str.session_state.current_chat_id = chat_id
            str.rerun()
            
    str.markdown("---")
    # User Account Info at the very bottom of sidebar
    str.markdown("👤 **පරිශීලක ගිණුම:** User Account")

# --- MAIN CHAT INTERFACE ---
str.title(f"🧠 Neshu AI")
str.caption(f"වත්මන් මාතෘකාව: {str.session_state.chats[current_id]['title']}")

# Securely fetch API Key from Render environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    str.error("🚨 Configuration Error: Gemini API Key එක සෙට් කරලා නැහැ. Please add GEMINI_API_KEY to Render Environment Variables.")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Display current active chat's messages
    for msg in str.session_state.chats[current_id]["messages"]:
        with str.chat_message(msg["role"]):
            str.markdown(msg["content"])

    # User input field
    if user_prompt := str.chat_input("Neshu AI ගෙන් මොනවද දැනගන්න ඕනේ?"):
        # Display user message
        with str.chat_message("user"):
            str.markdown(user_prompt)
        
        # Save to history of the CURRENT chat session
        str.session_state.chats[current_id]["messages"].append({"role": "user", "content": user_prompt})

        # Generate response from AI
        with str.chat_message("assistant"):
            message_placeholder = str.empty()
            try:
                full_prompt = f"You are Neshu AI, an omniscient, all-knowing smart AI assistant. Answer accurately as Neshu AI: {user_prompt}"
                response = model.generate_content(full_prompt)
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                # Save AI response to history of the CURRENT chat session
                str.session_state.chats[current_id]["messages"].append({"role": "assistant", "content": ai_response})
                
                # --- AUTOMATIC TOPIC/TITLE GENERATION ---
                # පළවෙනි ප්‍රශ්නය ඇහුවාම ඒ ප්‍රශ්නය ඇසුරෙන් AI එකෙන්ම මාතෘකාවක් හදාගන්න ලොජික් එක
                if str.session_state.chats[current_id]["title"] == "🆕 new chat":
                    # Generate a short 2-4 word title using Gemini
                    title_prompt = f"Based on this user query, generate a short 2 to 4 words title in Sinhala or English representing the topic. Query: {user_prompt}"
                    title_response = model.generate_content(title_prompt)
                    generated_title = title_response.text.strip().replace('"', '')
                    # Limit title length just in case
                    str.session_state.chats[current_id]["title"] = generated_title[:30]
                
                str.rerun() # Refresh to update sidebar titles immediately
                
            except Exception as e:
                str.error(f"Error එකක් වුණා: {str(e)}")

# --- DEVELOPER FOOTER ---
str.markdown(
    """
    <div class="footer">
        <p>👨‍💻 <b>Developer:</b> [vimukthi thuhina] | 📞 <b>Contact:</b> [94760762142]</p>
    </div>
    """,
    unsafe_allow_html=True
)
