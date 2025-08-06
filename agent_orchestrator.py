# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# def load_api_key():
#     load_dotenv()
#     key = os.getenv("GEMINI_API_KEY")
#     if not key:
#         raise ValueError("GEMINI_API_KEY not found in environment variables.")
#     genai.configure(api_key=key)

# def query_agent(text: str):
#     load_api_key()
#     prompt = f"""
# You are an expert agricultural AI assistant.
# User problem description: {text}
# Diagnose the probable issue (e.g., crop disease, pest) and ask clarifying questions to get more details.
# Provide actionable advice based on typical government schemes and sustainable farming.
# """
#     # Gemini models are synchronous
#     model = genai.GenerativeModel("gemini-1.5-pro-latest")
#     response = model.generate_content(prompt)
#     return response.text

import os
from dotenv import load_dotenv
import google.generativeai as genai

def load_api_key():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=key)

def query_agent(text: str):
    try:
        load_api_key()
        prompt = f"""
You are an expert agricultural AI assistant.
User problem description: {text}
Diagnose the probable issue (e.g., crop disease, pest) and ask clarifying questions to get more details.
Provide actionable advice based on typical government schemes and sustainable farming.
"""
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        if 'ResourceExhausted' in str(e) or 'quota' in str(e):
            return "❗ Quota limit reached for Gemini API. Please wait or try again later."
        else:
            return f"Error: {e}"
