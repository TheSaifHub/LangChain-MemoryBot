# from langchain.chains import ConversationChain
# from llm import llm
# from memory import get_memory

# def get_conversation_chain(session_id: str = "default_user"):
#     """
#     Returns a ConversationChain with persistent memory.
#     """

#     memory = get_memory(session_id)

#     conversation = ConversationChain(
#         llm=llm,
#         memory=memory,
#         verbose=True
#     )

#     return conversation

from langchain.chains import ConversationChain
from llm import llm
from memory import get_memory
from langchain.prompts import PromptTemplate

def get_conversation_chain(session_id: str = "default_user"):
    """
    Returns a ConversationChain with persistent memory
    and balanced response style.
    """

    memory = get_memory(session_id)

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template="""
You are a helpful and professional assistant.

Guidelines:
- Answer the user's question clearly and directly.
- Keep responses short and to the point.
- Add small helpful context only if it improves understanding.
- Do NOT over-explain.
- Do NOT mention training data, datasets, or internal details.

Conversation so far:
{history}

User: {input}
Assistant:
"""
    )

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=False
    )

    return conversation
