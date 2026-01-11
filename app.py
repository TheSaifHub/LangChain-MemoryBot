# from chain import get_conversation_chain

# print("✅ LangChainMemoryBot started")
# print("Type 'exit' to quit.\n")

# # Ask user for a username (used as session_id)
# user_id = input("Enter your username: ")

# # Create conversation with user-specific memory
# conversation = get_conversation_chain(session_id=user_id)

# while True:
#     query = input("\nYou: ")

#     if query.lower() in ["exit", "quit", "bye"]:
#         print("Bot: Bye bro! See you 👋")
#         break

#     response = conversation.predict(input=query)
#     print("Bot:", response)

# import streamlit as st
# from chain import get_conversation_chain

# # ---------------- Page Config ----------------
# st.set_page_config(
#     page_title="LangChain MemoryBot",
#     page_icon="🤖",
#     layout="centered"
# )

# # ---------------- Title ----------------
# st.title("🤖 LangChain MemoryBot")
# st.caption("Persistent AI Chatbot using LangChain + ChatGroq")

# # ---------------- Sidebar ----------------
# with st.sidebar:
#     st.header("👤 User Session")
#     user_id = st.text_input("Enter your username", placeholder="e.g. saif")
#     button_start = st.button("Start Chatting")
#     st.markdown("---")
#     st.markdown("### ℹ️ How it works")
#     st.markdown(
#         """
#         - Each user has **separate memory**
#         - Conversations are stored in a **database**
#         - Bot remembers you even after restart
#         """
#     )

# # ---------------- Session State ----------------
# if "conversation" not in st.session_state:
#     st.session_state.conversation = None

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ---------------- Start Chat ----------------
# if button_start and user_id:
#     st.session_state.conversation = get_conversation_chain(session_id=user_id)
#     st.success(f"Session started for **{user_id}**")

# # ---------------- Chat UI ----------------
# if st.session_state.conversation:

#     # Display previous messages
#     for role, message in st.session_state.messages:
#         with st.chat_message("user" if role == "user" else "assistant"):
#             st.markdown(message)

#     # Chat input
#     user_input = st.chat_input("Type your message...")

#     if user_input:
#         # Show user message
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         # Save user message
#         st.session_state.messages.append(("user", user_input))

#         # Get response from LangChain
#         response = st.session_state.conversation.predict(input=user_input)

#         # Show bot message
#         with st.chat_message("assistant"):
#             st.markdown(response)

#         # Save bot message
#         st.session_state.messages.append(("assistant", response))

# else:
#     st.info("👈 Enter your username in the sidebar to start chatting.")


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

# ---------------- Database Export Functions ----------------
# (Kept exactly the same as your code)
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

# ---------------- Session State Initialization ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "export_df" not in st.session_state:
    st.session_state.export_df = None

# ---------------- LOGIC FLOW ----------------

# CASE 1: USER IS NOT LOGGED IN (Show Login Screen on Main Page)
if not st.session_state.user_id:
    
    st.title("🤖 LangChain MemoryBot")
    st.markdown("### Welcome! 👋")
    st.write("Please enter your username to continue your conversation.")

    # Create a clean form for login
    with st.form("login_form"):
        username_input = st.text_input("Username", placeholder="e.g. saif")
        submit_button = st.form_submit_button("Start Chatting")

    if submit_button and username_input:
        # Save user to session
        st.session_state.user_id = username_input
        # Initialize Chain
        with st.spinner("Loading memory..."):
            st.session_state.conversation = get_conversation_chain(session_id=username_input)
            time.sleep(1) # UX pause
        st.rerun() # Refresh to show chat interface

# CASE 2: USER IS LOGGED IN (Show Chat UI)
else:
    # --- Sidebar for Tools (Only visible when logged in) ---
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

        # Download Button (Appears if data is ready)
        if st.session_state.export_df is not None:
            st.markdown("---")
            csv = st.session_state.export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=st.session_state.export_filename,
                mime="text/csv",
            )

    # --- Main Chat Interface ---
    st.subheader(f"Chatting as: {st.session_state.user_id}")
    
    # Display previous messages
    for role, message in st.session_state.messages:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(message)

    # Chat input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # 1. Display User Message
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append(("user", user_input))

        # 2. Generate Response
        if st.session_state.conversation:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.conversation.predict(input=user_input)
                    st.markdown(response)
            
            # 3. Save Assistant Message
            st.session_state.messages.append(("assistant", response))