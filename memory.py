from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import SQLChatMessageHistory

def get_memory(session_id: str = "default_user"):
    """
    Creates persistent memory using SQLite.
    Each session_id gets separate memory.
    """

    chat_history = SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_memory.db"
    )

    memory = ConversationBufferMemory(
        chat_memory=chat_history,
        return_messages=True
    )

    return memory
