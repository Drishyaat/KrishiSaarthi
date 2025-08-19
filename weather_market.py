import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load API key
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

def get_weather_advice(location: str):
    """
    Get AI-generated weather advice for farming based on location
    """
    try:
        prompt = f"""
You are an agricultural meteorologist. For the location "{location}", provide:

1. **Current Weather Assessment**: Describe likely current weather conditions for this region
2. **Agricultural Impact**: How these conditions affect crops and farming activities
3. **Actionable Advice**: Specific recommendations for farmers based on these conditions

Consider typical weather patterns for this location and provide practical farming advice.
Keep response concise but actionable.

Format:
Weather: [condition description]
Advice: [specific farming recommendations]
"""
        
        model = genai.GenerativeModel("gemini-1.5-flash")  # Using flash for faster response
        response = model.generate_content(prompt)
        
        # Parse response
        response_text = response.text
        weather_condition = "Weather analysis complete"
        advice = response_text
        
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith('Weather:'):
                weather_condition = line.replace('Weather:', '').strip()
            elif line.startswith('Advice:'):
                advice = line.replace('Advice:', '').strip()
        
        return weather_condition, advice
        
    except Exception as e:
        return "Weather service unavailable", f"Unable to get weather advice: {str(e)}"

def get_market_intelligence():
    """
    Get AI-generated market tips and insights for farmers
    """
    try:
        prompt = """
You are an agricultural market analyst. Provide a current, realistic market tip for farmers including:

1. **Market Trend**: A specific trend in agricultural commodities
2. **Actionable Insight**: What farmers should consider doing
3. **Timing Advice**: When to act on this information

Focus on practical, actionable advice that farmers can use for better profitability.
Keep it concise and specific.

Format: [One practical market tip with specific recommendations]
"""
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        return response.text.strip()
        
    except Exception as e:
        return f"Market intelligence unavailable: {str(e)}"

# Keep original function names for backward compatibility
def get_mock_weather(location: str):
    """Wrapper for backward compatibility"""
    return get_weather_advice(location)

def get_market_tip():
    """Wrapper for backward compatibility"""
    return get_market_intelligence()