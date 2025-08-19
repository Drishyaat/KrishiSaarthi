# import streamlit as st
# from PIL import Image

# # Import with error handling
# try:
#     from disease_detection import detect_disease_from_image
#     from agent_orchestrator import query_agent_with_context
#     from weather_market import get_mock_weather, get_market_tip
# except ImportError as e:
#     st.error(f"Import error: {e}")
#     st.stop()
# except ValueError as e:
#     st.error(f"Configuration error: {e}")
#     st.error("Please make sure GEMINI_API_KEY is set in your .env file")
#     st.stop()

# st.title("Farmer's Copilot AI - Crop Health Diagnosis and Advice")

# # Initialize session state for conversation
# if 'conversation_history' not in st.session_state:
#     st.session_state.conversation_history = []
# if 'current_mode' not in st.session_state:
#     st.session_state.current_mode = None  # 'text' or 'image'

# # Display conversation history
# if st.session_state.conversation_history:
#     st.subheader("💬 Conversation History")
#     for i, (user_msg, ai_response) in enumerate(st.session_state.conversation_history):
#         with st.expander(f"Exchange {i+1}", expanded=(i == len(st.session_state.conversation_history)-1)):
#             st.write(f"**You:** {user_msg}")
#             st.write(f"**AI:** {ai_response}")

# # User inputs
# uploaded_file = st.file_uploader("Upload Crop Image", type=["jpg", "jpeg", "png"])
# crop_issue_text = st.text_area("Describe your crop issue or answer the AI's questions:", 
#                                placeholder="e.g., yellow leaves, spots, or answer previous questions...")
# location = st.text_input("Enter your location (city or coordinates) for weather advice")

# # Clear conversation button
# if st.session_state.conversation_history:
#     if st.button("🔄 Start New Conversation"):
#         st.session_state.conversation_history = []
#         st.session_state.current_mode = None
#         st.rerun()

# if st.button("Get Diagnosis and Advice"):
#     if uploaded_file:
#         # Image mode
#         st.session_state.current_mode = 'image'
#         with st.spinner("Analyzing crop image..."):
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Crop Image", use_container_width=True)
#             disease, confidence, explanation = detect_disease_from_image(image)
            
#         st.subheader(f"Detected Disease: {disease}")
#         st.write(f"Confidence: {confidence * 100:.1f}%")
#         st.write(f"Explanation: {explanation}")

#         # Add to conversation history
#         user_msg = f"[Uploaded image] Disease detected: {disease}"
#         ai_response = f"Confidence: {confidence * 100:.1f}%. {explanation}"
#         st.session_state.conversation_history.append((user_msg, ai_response))

#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     elif crop_issue_text.strip():
#         # Text mode with context
#         st.session_state.current_mode = 'text'
        
#         with st.spinner("Getting AI response..."):
#             # Pass conversation history for context
#             resp = query_agent_with_context(crop_issue_text, st.session_state.conversation_history)
            
#         st.write("### AI Agent Response")
#         st.write(resp)

#         # Add to conversation history
#         st.session_state.conversation_history.append((crop_issue_text, resp))

#         if location:
#             weather_cond, weather_adv = get_mock_weather(location)
#             st.write(f"### Weather condition: {weather_cond}")
#             st.write(f"Advice: {weather_adv}")
#             market_tip = get_market_tip()
#             st.write(f"### Market Tip: {market_tip}")

#     else:
#         st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")

# # Show conversation status
# if st.session_state.conversation_history:
#     st.sidebar.write(f"💬 **Conversation:** {len(st.session_state.conversation_history)} exchanges")
#     st.sidebar.write(f"🔄 **Mode:** {st.session_state.current_mode}")
#     st.sidebar.write("*The AI will remember your previous questions and answers for better diagnosis.*")

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
            st.image(image, caption="Uploaded Crop Image", use_container_width=True)
            disease, confidence, explanation = detect_disease_from_image(image)
            
        st.subheader(f"Detected Disease: {disease}")
        st.write(f"Confidence: {confidence * 100:.1f}%")
        st.write(f"Explanation: {explanation}")

        # Add to conversation history
        user_msg = f"[Uploaded image] Disease detected: {disease}"
        ai_response = f"Confidence: {confidence * 100:.1f}%. {explanation}"
        st.session_state.conversation_history.append((user_msg, ai_response))

        if location:
            weather_cond, weather_adv = get_mock_weather(location, crop_issue_text)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip(crop_issue_text)
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
            weather_cond, weather_adv = get_mock_weather(location, crop_issue_text)
            st.write(f"### Weather condition: {weather_cond}")
            st.write(f"Advice: {weather_adv}")
            market_tip = get_market_tip(crop_issue_text)
            st.write(f"### Market Tip: {market_tip}")

    else:
        st.warning("Please upload an image or describe your crop issue to get diagnosis and advice.")

# Show conversation status
if st.session_state.conversation_history:
    st.sidebar.write(f"💬 **Conversation:** {len(st.session_state.conversation_history)} exchanges")
    st.sidebar.write(f"🔄 **Mode:** {st.session_state.current_mode}")
    st.sidebar.write("*The AI will remember your previous questions and answers for better diagnosis.*")

# Growing plant animation at bottom
st.markdown("""
<div style="text-align: center; margin-top: 3rem;">
    <style>
        .plant {
            display: inline-block;
            font-size: 3rem;
            animation: grow 3s ease-in-out infinite;
        }
        
        @keyframes grow {
            0% { transform: scale(0.8) translateY(10px); opacity: 0.7; }
            50% { transform: scale(1.1) translateY(-5px); opacity: 1; }
            100% { transform: scale(0.8) translateY(10px); opacity: 0.7; }
        }
        
        .soil {
            display: inline-block;
            font-size: 2rem;
            color: #8D6E63;
        }
    </style>
    <div class="soil">🟫🟫🟫🟫🟫</div><br>
    <div class="plant">🌱</div>
</div>
""", unsafe_allow_html=True)