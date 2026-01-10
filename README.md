🤖 LangChainMemoryBot

LangChainMemoryBot is a Streamlit-based AI chatbot built using LangChain and ChatGroq that supports persistent, multi-user conversation memory.
It remembers user information across sessions using a SQLite database, enabling contextual and personalized interactions even after app restarts.

------------------------------------------------------------------------------------------------------------------

🚀 Features

🧠 Persistent Memory – Remembers conversations across sessions using SQLite

👥 Multi-User Support – Each user has isolated memory using unique session IDs

⚡ Powered by ChatGroq – Fast and high-quality responses with LLaMA models

💬 Streamlit Chat UI – Clean, modern, and easy-to-use web interface

🔐 Secure API Handling – Uses environment variables for API keys

------------------------------------------------------------------------------------------------------------------

🏗️ Project Structure
LangChainMemoryBot/
│
├── app.py            # Streamlit UI
├── chain.py          # LangChain conversation logic
├── memory.py         # Persistent memory (SQLite)
├── llm.py            # ChatGroq model configuration
├── chat_memory.db    # Auto-generated database for memory
├── .env              # API key (not committed)
├── requirements.txt
└── README.md

------------------------------------------------------------------------------------------------------------------

🧠 How It Works

Each user is identified using a session ID (username).

Conversations are stored in a SQLite database (chat_memory.db).

When a user returns, their past messages are retrieved and passed back to the model.

This enables the chatbot to remember personal details like names, preferences, and previous context.

------------------------------------------------------------------------------------------------------------------

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/LangChainMemoryBot.git
cd LangChainMemoryBot

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
venv\Scripts\activate    # On Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

------------------------------------------------------------------------------------------------------------------

🔐 Environment Setup

Create a .env file in the project root:

GROQ_API_KEY=your_api_key_here

------------------------------------------------------------------------------------------------------------------

▶️ Run the Application
streamlit run app.py


Open in your browser:

http://localhost:8501

------------------------------------------------------------------------------------------------------------------

🧪 Example Usage

Enter your username (e.g., saif)

Chat with the bot:

My name is Saif
I am learning machine learning


Close the app.

Restart and use the same username:

What is my name?


➡ The bot responds: “Your name is Saif.”

------------------------------------------------------------------------------------------------------------------

📦 Tech Stack

Python

Streamlit

LangChain

ChatGroq (LLaMA models)

SQLite

python-dotenv

------------------------------------------------------------------------------------------------------------------

📌 Use Cases

Personal AI assistant with memory

Study and learning chatbot

Customer support prototype

AI projects demonstrating long-term context

------------------------------------------------------------------------------------------------------------------

🧑‍💻 Author

Saif Ibrahim
Aspiring Data Analyst | Machine Learning Enthusiast | AI Learner

------------------------------------------------------------------------------------------------------------------

📄 License

This project is open-source and available under the MIT License.