import streamlit as st  # මෙතන 'st' විදිහට වෙනස් කළා Python පැටලෙන්නේ නැති වෙන්න
import google.generativeai as genai
import os
import uuid

# Page configurations
st.set_page_config(page_title="Neshu AI", page_icon="https://raw.githubusercontent.com/https://raw.githubusercontent.com/ViSsapro/neshu-ai/refs/heads/main/1783829782373%7E2.pngViSsapro/neshu-ai/refs/heads/main/1783829782373~2.png", layout="centered")

# --- DARK MODE & STYLING CSS ---
st.markdown(
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
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# Function to start a brand new chat session
def start_new_chat():
    new_id = str(uuid.uuid4())  # දැන් මේක සුපිරියටම වැඩ කරනවා!
    st.session_state.chats[new_id] = {
        "title": "🆕 new chat",
        "messages": []
    }
    st.session_state.current_chat_id = new_id

# If there are no chats at all, create the first one automatically
if not st.session_state.chats or st.session_state.current_chat_id is None:
    start_new_chat()

current_id = st.session_state.current_chat_id

# --- SIDEBAR MENU SYSTEM ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/https://raw.githubusercontent.com/ViSsapro/neshu-ai/refs/heads/main/1783829782373%7E2.pngViSsapro/neshu-ai/refs/heads/main/1783829782373~2.png", width=80)
st.markdown("# Neshu AI")
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
        
    st.markdown("---")
    
    # Total Chat Count Display
    total_chats = len(st.session_state.chats)
    st.write(f"📊 **chat list:** {total_chats}")
    
    st.markdown("### 💬 CHAT LIST")
    
    # Displaying All Past Chats as individual clickable buttons
    for chat_id, chat_data in list(st.session_state.chats.items()):
        button_label = f"💬 {chat_data['title']}"
        if chat_id == current_id:
            button_label = f"▶️ {chat_data['title']} (Active)"
            
        if st.button(button_label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
    st.markdown("---")
    st.markdown("👤 **පරිශීලක ගිණුම:** User Account")

# --- MAIN CHAT INTERFACE ---
st.title(f"🧠 Neshu AI")
st.caption(f"now chat: {st.session_state.chats[current_id]['title']}")

# Securely fetch API Key from Render environment variables
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("🚨 Configuration Error: Gemini API Key එක සෙට් කරලා නැහැ. Please add GEMINI_API_KEY to Render Environment Variables.")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Display current active chat's messages
    for msg in st.session_state.chats[current_id]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input field
    if user_prompt := st.chat_input("Neshu AI ගෙන් මොනවද දැනගන්න ඕනේ?"):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        st.session_state.chats[current_id]["messages"].append({"role": "user", "content": user_prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                full_prompt = f"You are Neshu AI, an omniscient, all-knowing smart AI assistant. Answer accurately as Neshu AI: {user_prompt}"
                response = model.generate_content(full_prompt)
                ai_response = response.text
                message_placeholder.markdown(ai_response)
                
                st.session_state.chats[current_id]["messages"].append({"role": "assistant", "content": ai_response})
                
                # AUTOMATIC TOPIC/TITLE GENERATION
                if st.session_state.chats[current_id]["title"] == "🆕 නව සංවාදය":
                    title_prompt = f"Based on this user query, generate a short 2 to 4 words title in Sinhala or English representing the topic. Query: {user_prompt}"
                    title_response = model.generate_content(title_prompt)
                    generated_title = title_response.text.strip().replace('"', '')
                    st.session_state.chats[current_id]["title"] = generated_title[:30]
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error එකක් වුණා: {str(e)}")

# --- DEVELOPER FOOTER ---
st.markdown(
    """
    <div class="footer">
        <p>👨‍💻 <b>Developer:</b> [vimukthi thuhina] | 📞 <b>Contact:</b> [94760762142]</p>
    </div>
    """,
    unsafe_allow_html=True
)
