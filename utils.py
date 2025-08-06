from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")
