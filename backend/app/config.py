import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/vector_store")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/support.db")