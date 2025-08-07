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
#     try:
#         load_api_key()
#         prompt = f"""
# You are an expert agricultural AI assistant.
# User problem description: {text}
# Diagnose the probable issue (e.g., crop disease, pest) and ask clarifying questions to get more details.
# Provide actionable advice based on typical government schemes and sustainable farming.
# """
#         model = genai.GenerativeModel("gemini-1.5-pro-latest")
#         response = model.generate_content(prompt)
#         return response.text
#     except Exception as e:
#         if 'ResourceExhausted' in str(e) or 'quota' in str(e):
#             return "❗ Quota limit reached for Gemini API. Please wait or try again later."
#         else:
#             return f"Error: {e}"

import os
from dotenv import load_dotenv
import google.generativeai as genai
import time

# Load and configure API key once at module level
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

def query_agent(text: str, max_retries=3):
    """
    Original function for backward compatibility
    """
    return query_agent_with_context(text, [], max_retries)

def query_agent_with_context(text: str, conversation_history: list = None, max_retries=3):
    """
    Query the Gemini AI agent with conversation context
    """
    if conversation_history is None:
        conversation_history = []
    
    for attempt in range(max_retries):
        try:
            # Build context from conversation history
            context = ""
            if conversation_history:
                context = "Previous conversation:\n"
                for i, (user_msg, ai_response) in enumerate(conversation_history[-3:]):  # Last 3 exchanges
                    context += f"User: {user_msg}\n"
                    context += f"AI: {ai_response}\n"
                context += "\nContinuing the conversation...\n"
            
            prompt = f"""
You are an expert agricultural AI assistant helping a farmer diagnose crop issues.

{context}

Current user input: {text}

Instructions:
1. If this is a follow-up response to your previous questions, analyze the user's answer and provide more specific diagnosis.
2. If this seems like a new issue, start with initial assessment.
3. Ask specific, targeted follow-up questions only when needed for accurate diagnosis.
4. Once you have enough information, provide:
   - Likely diagnosis
   - Specific treatment recommendations
   - Prevention measures
   - Government schemes or resources if applicable

Keep responses concise and practical for farmers.
"""
            
            model = genai.GenerativeModel("gemini-1.5-pro-latest")
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_str = str(e).lower()
            
            if 'resourceexhausted' in error_str or 'quota' in error_str or 'rate limit' in error_str:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5  # Exponential backoff: 5, 10, 20 seconds
                    time.sleep(wait_time)
                    continue
                else:
                    return "❗ API quota limit reached. Please wait a few minutes and try again."
            
            elif 'invalid_argument' in error_str or 'permission' in error_str:
                return "❗ API configuration error. Please check your API key and permissions."
            
            else:
                return f"❗ Unexpected error: {str(e)}"
    
    return "❗ Failed to get response after multiple attempts. Please try again later."