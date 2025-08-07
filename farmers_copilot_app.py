
# import streamlit as st
# from PIL import Image
# import os

# from disease_detection import detect_disease_from_image
# from agent_orchestrator import query_agent  
# from weather_market import get_mock_weather, get_market_tip

# st.title("Farmer's Copilot AI - Crop Health Diagnosis and Advice")

# uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
# crop_issue_text = st.text_area("Or describe your crop issue here (e.g. yellow leaves, spots)")

# if st.button("Get Diagnosis and Advice"):
#     if uploaded_file:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Crop Image", use_column_width=True)
#         disease, confidence, explanation = detect_disease_from_image(image)
#         st.subheader(f"Detected Disease: {disease}")
#         st.write(f"Confidence: {confidence * 100}%")
#         st.write(f"Explanation: {explanation}")

#         location = st.text_input("Enter your location (city or coordinates) for weather advice")
#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     elif crop_issue_text.strip():
#         st.write(f"You described: {crop_issue_text}")
#         resp = query_agent(crop_issue_text)
#         st.write("### AI Agent Response")
#         st.write(resp)

#         location = st.text_input("Enter your location (city or coordinates) for weather advice")
#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     else:
#         st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")

#2
# import streamlit as st
# from PIL import Image

# from disease_detection import detect_disease_from_image
# from agent_orchestrator import query_agent
# from weather_market import get_mock_weather, get_market_tip

# st.title("Farmer's Copilot AI - Crop Health Diagnosis and Advice")

# # User inputs (not inside button)
# uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
# crop_issue_text = st.text_area("Or describe your crop issue here (e.g. yellow leaves, spots)")
# location = st.text_input("Enter your location (city or coordinates) for weather advice")

# if st.button("Get Diagnosis and Advice"):
#     if uploaded_file:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Crop Image", use_column_width=True)
#         disease, confidence, explanation = detect_disease_from_image(image)
#         st.subheader(f"Detected Disease: {disease}")
#         st.write(f"Confidence: {confidence * 100}%")
#         st.write(f"Explanation: {explanation}")

#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     elif crop_issue_text.strip():
#         st.write(f"You described: {crop_issue_text}")
#         resp = query_agent(crop_issue_text)
#         st.write("### AI Agent Response")
#         st.write(resp)

#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     else:
#         st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")

import streamlit as st
from PIL import Image

# Import with error handling
try:
    from disease_detection import detect_disease_from_image
    from agent_orchestrator import query_agent_with_context
    from weather_market import get_mock_weather, get_market_tip
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()
except ValueError as e:
    st.error(f"Configuration error: {e}")
    st.error("Please make sure GEMINI_API_KEY is set in your .env file")
    st.stop()

st.title("Farmer's Copilot AI - Crop Health Diagnosis and Advice")

# Initialize session state for conversation
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None  # 'text' or 'image'

# Display conversation history
if st.session_state.conversation_history:
    st.subheader("💬 Conversation History")
    for i, (user_msg, ai_response) in enumerate(st.session_state.conversation_history):
        with st.expander(f"Exchange {i+1}", expanded=(i == len(st.session_state.conversation_history)-1)):
            st.write(f"**You:** {user_msg}")
            st.write(f"**AI:** {ai_response}")

# User inputs
uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
crop_issue_text = st.text_area("Describe your crop issue or answer the AI's questions:", 
                               placeholder="e.g., yellow leaves, spots, or answer previous questions...")
location = st.text_input("Enter your location (city or coordinates) for weather advice")

# Clear conversation button
if st.session_state.conversation_history:
    if st.button("🔄 Start New Conversation"):
        st.session_state.conversation_history = []
        st.session_state.current_mode = None
        st.rerun()

if st.button("Get Diagnosis and Advice"):
    if uploaded_file:
        # Image mode
        st.session_state.current_mode = 'image'
        with st.spinner("Analyzing crop image..."):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Crop Image", use_column_width=True)
            disease, confidence, explanation = detect_disease_from_image(image)
            
        st.subheader(f"Detected Disease: {disease}")
        st.write(f"Confidence: {confidence * 100:.1f}%")
        st.write(f"Explanation: {explanation}")

        # Add to conversation history
        user_msg = f"[Uploaded image] Disease detected: {disease}"
        ai_response = f"Confidence: {confidence * 100:.1f}%. {explanation}"
        st.session_state.conversation_history.append((user_msg, ai_response))

        if location:
            weather_cond, weather_adv = get_mock_weather(location)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip()
            st.write(f"### Market Tip: {market_tip}")

    elif crop_issue_text.strip():
        # Text mode with context
        st.session_state.current_mode = 'text'
        
        with st.spinner("Getting AI response..."):
            # Pass conversation history for context
            resp = query_agent_with_context(crop_issue_text, st.session_state.conversation_history)
            
        st.write("### AI Agent Response")
        st.write(resp)

        # Add to conversation history
        st.session_state.conversation_history.append((crop_issue_text, resp))

        if location:
            weather_cond, weather_adv = get_mock_weather(location)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip()
            st.write(f"### Market Tip: {market_tip}")

    else:
        st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")

# Show conversation status
if st.session_state.conversation_history:
    st.sidebar.write(f"💬 **Conversation:** {len(st.session_state.conversation_history)} exchanges")
    st.sidebar.write(f"🔄 **Mode:** {st.session_state.current_mode}")
    st.sidebar.write("*The AI will remember your previous questions and answers for better diagnosis.*")