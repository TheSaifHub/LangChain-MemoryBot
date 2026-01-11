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

# ---------------- Page Config ----------------
st.set_page_config(page_title="LangChain MemoryBot", page_icon="🤖", layout="centered")


# ---------------- Database Export Functions ----------------
def parse_message(msg):
    try:
        # If already a dict
        if isinstance(msg, dict):
            msg_type = msg.get("type")
            data = msg.get("data", {})
            content = data.get("content")
            return msg_type, content

        # If stored as JSON string
        data = json.loads(msg)
        msg_type = data.get("type")
        content = data.get("data", {}).get("content")
        return msg_type, content

    except Exception:
        return None, None


def get_user_chat(session_id):
    try:
        conn = sqlite3.connect("chat_memory.db")

        query = """
        SELECT session_id, message
        FROM message_store
        WHERE session_id = ?
        ORDER BY id
        """

        df = pd.read_sql_query(query, conn, params=(session_id,))
        conn.close()

        if df.empty:
            return df

        # Parse message safely
        df[["role", "content"]] = df["message"].apply(
            lambda x: pd.Series(parse_message(x))
        )

        return df[["session_id", "role", "content"]]

    except Exception as e:
        st.error(f"Error reading database: {e}")
        return None


def get_all_chats():
    try:
        conn = sqlite3.connect("chat_memory.db")

        query = """
        SELECT session_id, message
        FROM message_store
        ORDER BY session_id, id
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return df

        # Parse message safely
        df[["role", "content"]] = df["message"].apply(
            lambda x: pd.Series(parse_message(x))
        )

        return df[["session_id", "role", "content"]]

    except Exception as e:
        st.error(f"Error reading database: {e}")
        return None


# ---------------- Title ----------------
st.title("🤖 LangChain MemoryBot")
st.caption("Persistent AI Chatbot using LangChain + ChatGroq")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("👤 User Session")
    user_id = st.text_input("Enter your username", placeholder="e.g. saif")
    button_start = st.button("Start Chatting")

    st.markdown("---")
    st.markdown("### ℹ️ How it works")

    export_user_button = st.button("Download My Chat (CSV)")
    export_all_button = st.button("Download All Chats (CSV)")

    st.markdown(
        """
        - Each user has **separate memory**
        - Conversations are stored in a **database**
        - Bot remembers you even after restart
        """
    )

# ---------------- Session State ----------------
if "conversation" not in st.session_state:
    st.session_state.conversation = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "export_df" not in st.session_state:
    st.session_state.export_df = None

if "export_filename" not in st.session_state:
    st.session_state.export_filename = None


# ---------------- Export Buttons ----------------
if export_user_button:
    if not user_id:
        st.warning("Please enter your username first.")
    else:
        df = get_user_chat(user_id)
        if df is not None and not df.empty:
            st.session_state.export_df = df
            st.session_state.export_filename = f"{user_id}_chat_history.csv"
            st.success("Your chat is ready to download below ⬇️")
        else:
            st.info("No chat history found for this user.")

if export_all_button:
    df = get_all_chats()
    if df is not None and not df.empty:
        st.session_state.export_df = df
        st.session_state.export_filename = "all_users_chat_history.csv"
        st.success("All chat data is ready to download below ⬇️")
    else:
        st.info("No chat history found in the database.")


# ---------------- Download Section ----------------
if st.session_state.export_df is not None:
    csv = st.session_state.export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=st.session_state.export_filename,
        mime="text/csv",
    )


# ---------------- Start Chat ----------------
if button_start and user_id:
    st.session_state.conversation = get_conversation_chain(session_id=user_id)
    st.success(f"Session started for **{user_id}**")


# ---------------- Chat UI ----------------
if st.session_state.conversation:

    # Display previous messages
    for role, message in st.session_state.messages:
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(message)

    # Chat input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Save user message
        st.session_state.messages.append(("user", user_input))

        # Get response from LangChain
        response = st.session_state.conversation.predict(input=user_input)

        # Show bot message
        with st.chat_message("assistant"):
            st.markdown(response)

        # Save bot message
        st.session_state.messages.append(("assistant", response))

else:
    st.info("👈 Enter your username in the sidebar to start chatting.")
