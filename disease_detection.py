import os
import base64
import io
from PIL import Image
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

def image_to_base64(image: Image.Image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def detect_disease_from_image(image: Image.Image):
    """
    Use Gemini Vision to analyze crop images for diseases
    """
    try:
        # Resize image if too large (Gemini has size limits)
        if image.width > 1024 or image.height > 1024:
            image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        prompt = """
You are an expert agricultural pathologist and crop disease specialist. Analyze this crop image and provide:

1. **Disease/Condition Name**: Most likely disease or health condition
2. **Confidence Level**: Your confidence in this diagnosis (0.0 to 1.0)
3. **Detailed Explanation**: What symptoms you observe and why you think it's this condition

Focus on:
- Leaf discoloration, spots, patterns
- Plant structure abnormalities  
- Signs of pests or fungal infections
- Overall plant health indicators

If the image is unclear or doesn't show a plant, mention that.

Format your response as:
Disease: [disease name]
Confidence: [0.0-1.0]
Explanation: [detailed analysis]
"""
        
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content([prompt, image])
        
        # Parse the response
        response_text = response.text
        
        # Extract information using simple parsing
        disease = "Unknown"
        confidence = 0.5
        explanation = response_text
        
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith('Disease:'):
                disease = line.replace('Disease:', '').strip()
            elif line.startswith('Confidence:'):
                try:
                    conf_str = line.replace('Confidence:', '').strip()
                    confidence = float(conf_str)
                except:
                    confidence = 0.5
            elif line.startswith('Explanation:'):
                explanation = line.replace('Explanation:', '').strip()
        
        # If parsing failed, use the full response as explanation
        if disease == "Unknown":
            explanation = response_text
            disease = "Analysis Complete"
            confidence = 0.8
            
        return disease, confidence, explanation
        
    except Exception as e:
        error_msg = str(e).lower()
        if 'quota' in error_msg or 'rate limit' in error_msg:
            return "API Limit Reached", 0.0, "Please wait a few minutes before trying again."
        else:
            return "Analysis Failed", 0.0, f"Error analyzing image: {str(e)}"