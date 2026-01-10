from langchain_groq import ChatGroq
import streamlit as st


# ---------------- Load API Key for using locally ---------------- 
# from dotenv import load_dotenv
# import os

# Load environment variables
# load_dotenv()

# groq_api_key = os.getenv("GROQ_API_KEY")

# ---------------- Load API Key for deploying on streamlit ----------------
groq_api_key = st.secrets["API_KEY"]

# ---------------- Validate API Key ----------------
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.4,
    api_key=groq_api_key,
    max_tokens=512,
)
