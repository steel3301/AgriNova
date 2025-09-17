import streamlit as st
import crop_planner
import market_linkage
import requests
import pandas as pd
import json
import dotenv
import google.generativeai as genai
import tempfile
from gtts import gTTS
import os
from PIL import Image

dotenv.load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
# ------------------------------
# Farming Assistant Page
# ------------------------------
def run_digital_farming_assistant():
    # ------------------ CONFIG ------------------
    st.set_page_config(
        page_title="AI Farming Assistant",
        page_icon="🌾",
        layout="wide"
    )

    st.title("🌾 AI-Powered Digital Farming Assistant")
    st.markdown("Get instant, detailed answers to all your farming questions!")

    # ------------------ GEMINI CONFIG ------------------
    genai.configure(api_key="GEMINI_API_KEY")

    # ------------------ SESSION STATE ------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "queries_log" not in st.session_state:
        st.session_state.queries_log = pd.DataFrame(columns=["Timestamp", "Question", "Answer"])


    # ------------------ FUNCTIONS ------------------
    def get_gemini_response(query, chat_history=[]):
        """Fetch detailed AI response from Gemini."""
        try:
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            # Build conversation context
            conversation = "You are an expert agricultural assistant helping farmers.\nProvide detailed step-by-step advice and multiple solutions if possible.\n\n"
            for chat in chat_history[-10:]:
                role = "Farmer" if chat["role"] == "user" else "Assistant"
                conversation += f"{role}: {chat['content']}\n"
            conversation += f"Farmer: {query}\nAssistant:"
            response = model.generate_content(contents=conversation)
            return response.text.strip()
        except Exception as e:
            return "Sorry, something went wrong. Please try again later."


    def text_to_speech(text):
        """Convert text to speech using gTTS"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text)
        tts.save(temp_file.name)
        return temp_file.name


    # ------------------ SIDEBAR ------------------
    with st.sidebar:
        st.header("📋 Features")
        st.info("""
        - 🐛 Pest & Disease Management
        - 🌱 Crop Health Issues
        - 💧 Irrigation Planning
        - 🥼 Fertilizer Recommendations
        - 🌍 Soil Management
        - 📈 Market Information
        - 🚜 Modern Farming Techniques
        - 📱 Government Schemes
        """)
        st.header("⚙ Settings")
        voice_mode = st.checkbox("Enable Voice Output", value=True)
        show_dashboard = st.checkbox("Show Query Dashboard", value=True)
        if st.button("Clear Chat"):
            st.session_state.chat_history = []

    # ------------------ IMAGE UPLOAD ------------------
    uploaded_image = st.file_uploader("Upload an image related to your problem (optional)", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # ------------------ CHAT INPUT ------------------
    query_input = st.text_input("Ask your farming question:")
    send_button = st.button("Send")

    if (send_button and query_input):
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "content": query_input})

        with st.spinner("🤔 Thinking..."):
            # Get detailed AI response
            answer = get_gemini_response(query_input, st.session_state.chat_history)

        # Append AI response
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Add to queries dashboard
        st.session_state.queries_log = pd.concat([
            st.session_state.queries_log,
            pd.DataFrame([{"Timestamp": datetime.now(), "Question": query_input, "Answer": answer}])
        ], ignore_index=True)

        # Voice output
        if voice_mode:
            audio_file = text_to_speech(answer)
            st.audio(audio_file, format="audio/mp3")

        st.rerun()

    # ------------------ DISPLAY CHAT ------------------
    for chat in st.session_state.chat_history:
        color = "#e8f5e9" if chat["role"] == "user" else "#f5f5f5"
        st.markdown(
            f'<div style="padding:10px;margin:5px;border-left:4px solid; background:{color}">'
            f"<b>{'You' if chat['role'] == 'user' else 'Assistant'}:</b><br>{chat['content']}</div>",
            unsafe_allow_html=True
        )

    # ------------------ QUERY DASHBOARD ------------------
    if show_dashboard and not st.session_state.queries_log.empty:
        st.markdown("---")
        st.subheader("📊 Query Dashboard")
        st.dataframe(st.session_state.queries_log)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#666;'>💡 Tip: Be specific about crop type, location, and symptoms for better advice | 📞 Kisan Helpline: 1800-180-1551</div>",
        unsafe_allow_html=True
    )
# ------------------------------
# Main App with Sidebar
# ------------------------------
def main():
    st.sidebar.title("🌱 Navigation")
    page = st.sidebar.radio("Go to", ["Digital Farming Assistant", "Crop Planning", "Market Linkage & Price Forecasting"])

    if page == "Digital Farming Assistant":
        run_digital_farming_assistant()
    elif page == "Crop Planning":
        crop_planner.run_crop_planner()
    elif page == "Market Linkage & Price Forecasting":
        market_linkage.run_market_linkage()

if __name__ == "__main__":
    main()
