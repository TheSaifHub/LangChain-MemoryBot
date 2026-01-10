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

import streamlit as st
from chain import get_conversation_chain

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="LangChain MemoryBot",
    page_icon="🤖",
    layout="centered"
)

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
