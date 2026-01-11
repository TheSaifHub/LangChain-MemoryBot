import streamlit as st
from chain import get_conversation_chain
import sqlite3
import pandas as pd
import json
import time

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="LangChain MemoryBot", 
    page_icon="🤖", 
    layout="centered"
)

# ---------------- Database Functions ----------------
def parse_message(msg):
    try:
        if isinstance(msg, dict):
            msg_type = msg.get("type")
            data = msg.get("data", {})
            content = data.get("content")
            return msg_type, content
        data = json.loads(msg)
        msg_type = data.get("type")
        content = data.get("data", {}).get("content")
        return msg_type, content
    except Exception:
        return None, None

def get_user_chat(session_id):
    try:
        conn = sqlite3.connect("chat_memory.db")
        query = "SELECT session_id, message FROM message_store WHERE session_id = ? ORDER BY id"
        df = pd.read_sql_query(query, conn, params=(session_id,))
        conn.close()
        if df.empty: return df
        df[["role", "content"]] = df["message"].apply(lambda x: pd.Series(parse_message(x)))
        return df[["session_id", "role", "content"]]
    except Exception as e:
        st.error(f"Error reading database: {e}")
        return None

def get_all_chats():
    try:
        conn = sqlite3.connect("chat_memory.db")
        query = "SELECT session_id, message FROM message_store ORDER BY session_id, id"
        df = pd.read_sql_query(query, conn)
        conn.close()
        if df.empty: return df
        df[["role", "content"]] = df["message"].apply(lambda x: pd.Series(parse_message(x)))
        return df[["session_id", "role", "content"]]
    except Exception as e:
        st.error(f"Error reading database: {e}")
        return None

# ---------------- Session State ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "export_df" not in st.session_state:
    st.session_state.export_df = None

# ==========================================
#              LOGIC FLOW
# ==========================================

# CASE 1: USER IS NOT LOGGED IN (Login Screen)
if not st.session_state.user_id:
    
    st.title("🤖 LangChain MemoryBot")
    st.markdown("### Welcome! 👋")
    st.write("Please enter your username to continue your conversation.")

    # Login Form
    with st.form("login_form"):
        username_input = st.text_input("Username", placeholder="e.g. saif")
        submit_button = st.form_submit_button("Start Chatting")

    if submit_button and username_input:
        st.session_state.user_id = username_input
        with st.spinner("Loading memory..."):
            st.session_state.conversation = get_conversation_chain(session_id=username_input)
            time.sleep(1) 
        st.rerun()

    # --- FOOTER FOR LOGIN SCREEN (Fixed to Bottom, No Scroll) ---
    st.markdown(
        """
        <style>
        .footer-login {
            position: fixed;
            left: 0;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: #888;
            font-size: 14px;
            pointer-events: none; /* Allows clicking through empty space */
        }
        .footer-login a {
            color: #888;
            text-decoration: none;
            pointer-events: auto; /* Re-enable clicks on links */
        }
        .footer-login a:hover {
            color: #555;
            text-decoration: underline;
        }
        </style>
        <div class="footer-login">
            <p>Copyright © 2025 LangChain MemoryBot | Made with ❤️ by <a href="https://saifibrahim.netlify.app/" target="_blank"><b>Saif Ibrahim</b></a></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# CASE 2: USER IS LOGGED IN (Chat UI)
else:
    # --- Sidebar (Tools + Footer) ---
    with st.sidebar:
        st.header(f"👤 {st.session_state.user_id}")
        
        if st.button("Logout"):
            st.session_state.user_id = None
            st.session_state.conversation = None
            st.session_state.messages = []
            st.rerun()
            
        st.divider()
        st.markdown("### 🛠️ Tools")
        
        # Export Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("My Data"):
                df = get_user_chat(st.session_state.user_id)
                if df is not None and not df.empty:
                    st.session_state.export_df = df
                    st.session_state.export_filename = f"{st.session_state.user_id}_history.csv"
                else:
                    st.toast("No history found.")
        with col2:
            if st.button("All Data"):
                df = get_all_chats()
                if df is not None and not df.empty:
                    st.session_state.export_df = df
                    st.session_state.export_filename = "all_users_history.csv"
                else:
                    st.toast("No DB data found.")

        if st.session_state.export_df is not None:
            st.markdown("---")
            csv = st.session_state.export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=st.session_state.export_filename,
                mime="text/csv",
            )
        
        # --- FOOTER FOR CHAT SCREEN (Inside Sidebar) ---
        # Moving it here prevents overlap with the chat input on mobile
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; color: #888; font-size: 13px;">
                <p>Copyright © 2025 LangChain MemoryBot</p>
                <p>Made with ❤️ by <a href="https://saifibrahim.netlify.app/" target="_blank" style="color: #888;"><b>Saif Ibrahim</b></a></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Main Chat Area ---
    st.subheader(f"Chatting as: {st.session_state.user_id}")
    
    # Display Messages
    for role, message in st.session_state.messages:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(message)

    # Chat Input
    user_input = st.chat_input("Type your message...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append(("user", user_input))

        if st.session_state.conversation:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation.predict(input=user_input)
                    st.markdown(response)
            st.session_state.messages.append(("assistant", response))