
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


import streamlit as st
from PIL import Image

from disease_detection import detect_disease_from_image
from agent_orchestrator import query_agent
from weather_market import get_mock_weather, get_market_tip

st.title("Farmer's Copilot AI - Crop Health Diagnosis and Advice")

# User inputs (not inside button)
uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
crop_issue_text = st.text_area("Or describe your crop issue here (e.g. yellow leaves, spots)")
location = st.text_input("Enter your location (city or coordinates) for weather advice")

if st.button("Get Diagnosis and Advice"):
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Crop Image", use_column_width=True)
        disease, confidence, explanation = detect_disease_from_image(image)
        st.subheader(f"Detected Disease: {disease}")
        st.write(f"Confidence: {confidence * 100}%")
        st.write(f"Explanation: {explanation}")

        if location:
            weather_cond, weather_adv = get_mock_weather(location)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip()
            st.write(f"### Market Tip: {market_tip}")

    elif crop_issue_text.strip():
        st.write(f"You described: {crop_issue_text}")
        resp = query_agent(crop_issue_text)
        st.write("### AI Agent Response")
        st.write(resp)

        if location:
            weather_cond, weather_adv = get_mock_weather(location)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip()
            st.write(f"### Market Tip: {market_tip}")

    else:
        st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")
