import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import streamlit as st

# Load and configure API key once at module level
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
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
    Query the Gemini AI agent with conversation context for agricultural advice
    """
    if conversation_history is None:
        conversation_history = []
    
    for attempt in range(max_retries):
        try:
            # Build context from conversation history
            context = ""
            if conversation_history:
                context = "Previous conversation context:\n"
                for i, (user_msg, ai_response) in enumerate(conversation_history[-3:]):  # Last 3 exchanges
                    context += f"Farmer: {user_msg}\n"
                    context += f"Agricultural AI: {ai_response}\n"
                context += "\n--- Continuing conversation ---\n"
            
            prompt = f"""
You are an expert agricultural AI assistant with deep knowledge of:
- Crop diseases and pest management
- Soil health and nutrition
- Irrigation and water management
- Seasonal farming practices
- Government agricultural schemes
- Sustainable farming techniques
- Market trends and crop planning

{context}

Current farmer input: {text}

Guidelines for response:
1. If this is answering your previous questions, provide specific diagnosis and actionable treatment plans
2. If this is a new issue, ask 2-3 targeted questions to gather essential information
3. Always provide practical, implementable advice
4. Mention relevant government schemes or subsidies when applicable
5. Consider regional farming practices and local conditions
6. Keep responses farmer-friendly (avoid overly technical jargon)

Provide specific, actionable advice that farmers can implement immediately.
"""
            
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
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
                    return "❗ API quota limit reached. Please wait a few minutes and try again. Our agricultural AI is temporarily busy helping other farmers."
            
            elif 'invalid_argument' in error_str or 'permission' in error_str:
                return "❗ API configuration error. Please contact support if this issue persists."
            
            else:
                return f"❗ Temporary service issue. Please try again. Error details: {str(e)}"
    
    return "❗ Unable to connect to agricultural AI service after multiple attempts. Please try again in a few minutes."