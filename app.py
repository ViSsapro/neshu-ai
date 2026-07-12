import streamlit as st
import google.generativeai as genai
import os
import uuid

# ==========================================
# 🌟 ඔයාගේ ෆොටෝ එක සෙට් කරන ප්‍රධාන තැන 🌟
# ==========================================
# දැනට මම මේකට default ලෝගෝ ලින්ක් එකක් දාලා තියෙන්නේ. 
# ඔයාගේ GitHub එකට අප්ලෝඩ් කරපු ෆොටෝ එකේ ලින්ක් එක මේ පහළ තියෙන එක වෙනුවට ඩබල් කොටේෂන් ඇතුළට paste කරන්න.
AI_LOGO_URL = "https://raw.githubusercontent.com/https://raw.githubusercontent.com/ViSsapro/neshu-ai/refs/heads/main/1783829782373%7E2.pngViSsapro/neshu-ai/refs/heads/main/1783829782373~2.png"


# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Neshu AI", 
    page_icon=AI_LOGO_URL,  # බ්‍රවුසර් ටැබ් එකේ උඩින්ම පෙනෙන රූපය (Favicon)
    layout="centered"
)

# --- 2. DARK MODE & STYLING CSS ---
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
    section[data-testid="stSidebar"] {
        background-color: #181C24 !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p {
        color: #FAFAFA !important;
    }
    /* Search Bar එකට පහළින් පෙනෙන Footer එක සඳහා CSS */
    .custom-footer {
        text-align: center;
        color: #888888 !important;
        font-size: 13px;
        margin-top: 12px;
        margin-bottom: 5px;
        width: 100%;
        font-family: sans-serif;
    }
    .custom-footer a {
        color: #25D366 !important;
        text-decoration: none;
        font-weight: bold;
    }
    .custom-footer a:hover {
        text-decoration: underline;
    }
    /* Main title layout custom styles */
    .title-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 5px;
    }
    .title-container img {
        border-radius: 8px;
    }
    .sidebar-title-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. INITIALIZE SESSION STATE FOR MULTIPLE CHATS ---
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

def start_new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "🆕 නව සංවාදය",
        "messages": []
    }
    st.session_state.current_chat_id = new_id

if not st.session_state.chats or st.session_state.current_chat_id is None:
    start_new_chat()

current_id = st.session_state.current_chat_id

# --- 4. SIDEBAR MENU SYSTEM ---
with st.sidebar:
    # වම් පැත්තේ මෙනු එකේ උඩින්ම ඔයාගේ ෆොටෝ එක සහ නම පෙන්වීම
    st.markdown(
        f"""
        <div class="sidebar-title-container">
            <img src="{AI_LOGO_URL}" width="40" style="border-radius: 5px;">
            <h1 style="margin: 0; font-size: 25px;">Neshu AI</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        start_new_chat()
        st.rerun()
        
    st.markdown("---")
    
    # Total Chat Count Display
    total_chats = len(st.session_state.chats)
    st.write(f"📊 **ඔබගේ සමස්ත චැට් ගණන:** {total_chats}")
    
    st.markdown("### 💬 CHAT LIST")
    
    # Displaying All Past Chats
    for chat_id, chat_data in list(st.session_state.chats.items()):
        button_label = f"💬 {chat_data['title']}"
        if chat_id == current_id:
            button_label = f"▶️ {chat_data['title']} (Active)"
            
        if st.button(button_label, key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
    st.markdown("---")
    st.markdown("👤 **පරිශීලක ගිණුම:** User Account")

# --- 5. MAIN CHAT INTERFACE ---
# ප්‍රධාන පිටුවේ මැද පෙනෙන ලෝගෝ එක සහ Title එක
st.markdown(
    f"""
    <div class="title-container">
        <img src="{AI_LOGO_URL}" width="55">
        <h1 style="margin: 0;">Neshu AI</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.caption(f"වත්මන් මාතෘකාව: {st.session_state.chats[current_id]['title']}")

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
                if st.session_state.chats[current_id]["title"] == "🆕 new chat":
                    title_prompt = f"Based on this user query, generate a short 2 to 4 words title in Sinhala or English representing the topic. Query: {user_prompt}"
                    title_response = model.generate_content(title_prompt)
                    generated_title = title_response.text.strip().replace('"', '')
                    st.session_state.chats[current_id]["title"] = generated_title[:30]
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error එකක් වුණා: {str(e)}")

# --- 6. DEVELOPER FOOTER (SEARCH BAR එකට පහළින්) ---
DEVELOPER_NAME = "vimukthi thuhina wijerathna"            # ඔයාගේ නම මෙතනට දාන්න
WHATSAPP_NUMBER = "94760762142"     # මුලට 0 නැතුව ලංකාවේ කෝඩ් එක (94) සමග WhatsApp අංකය දාන්න
DISPLAY_NUMBER = "0760762142"       # පිටුවේ මිනිස්සුන්ට පේන්න තියෙන අංකය දාන්න

st.markdown(
    f"""
    <div class="custom-footer">
        👨‍💻 <b>Developer:</b> vimukthi thuhina wijerathna | 
        📞 <b>Contact:</b> <a href="https://wa.me/94760762142" target="_blank">0760762142 (WhatsApp 💬)</a>
    </div>
    """,
    unsafe_allow_html=True
)
