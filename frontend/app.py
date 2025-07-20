import streamlit as st
import requests
import json
import base64
import os
from typing import Optional


st.set_page_config(page_title="Conversational Time Machine", page_icon="🎙️", layout="wide")

# Function to get base64 image
def get_base64_image(path: str) -> Optional[str]:
    """Convert image to base64 string"""
    try:
        with open(path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    except FileNotFoundError:
        return None

# To load the images and convert to Base64
indira_img = get_base64_image("assets/indira gandhi.jpg")
atal_img = get_base64_image("assets/atal bihari vajpayee.jpeg")

# API configuration
API_URL = os.getenv("API_URL", "https://conversational-time-machine-project.onrender.com/api/chat/")


# Persona data
PERSONAS = {
    "indira": {
        "name": "Indira Gandhi",
        "desc": "First female Prime Minister of India (1966–1984). Known for decisive leadership and her role in shaping modern India.",
        "image": indira_img,
        "placeholder": "e.g., What was your role in the Bangladesh Liberation War?"
    },
    "atal": {
        "name": "Atal Bihari Vajpayee", 
        "desc": "Former Prime Minister (1998–2004), statesman, poet, and visionary leader known for his oratory skills.",
        "image": atal_img,
        "placeholder": "e.g., What inspired your poetry and political philosophy?"
    }
}

# Initialize session state
if 'selected_persona' not in st.session_state:
    st.session_state.selected_persona = ""
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Custom CSS for styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #b0b0b0;
        text-align: center;
        margin-bottom: 50px;
        font-weight: 300;
    }
    
    .persona-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }
    
    .persona-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .persona-image {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid rgba(255, 255, 255, 0.2);
    }
    
    .persona-name {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .persona-desc {
        color: #b0b0b0;
        line-height: 1.6;
    }
    
    .response-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        margin: 20px 0;
    }
    
    .response-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #4ecdc4;
        margin-bottom: 15px;
    }
    
    .response-text {
        color: #e0e0e0;
        line-height: 1.8;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        padding: 12px 40px !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stAudio > div {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🎙️ Conversational Time Machine</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Chat with historical leaders and hear their voice in real-time!</p>', unsafe_allow_html=True)


col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Choose a historical figure:")
    persona_options = [""] + list(PERSONAS.keys())
    persona_names = ["Select a leader..."] + [PERSONAS[key]["name"] for key in PERSONAS.keys()]
    
    selected_index = st.selectbox(
        "Historical Figure",
        range(len(persona_options)),
        format_func=lambda x: persona_names[x],
        label_visibility="collapsed"
    )
    
    if selected_index > 0:
        st.session_state.selected_persona = persona_options[selected_index]
    else:
        st.session_state.selected_persona = ""

with col2:
    if st.session_state.selected_persona:
        persona_data = PERSONAS[st.session_state.selected_persona]
        
        # Created the persona card
        persona_card_html = f"""
        <div class="persona-card">
            <div class="persona-header">
                <div class="persona-image">
                    {"<img src='" + persona_data["image"] + "' style='width: 100%; height: 100%; object-fit: cover; border-radius: 50%;' />" if persona_data["image"] else ""}
                </div>
                <div>
                    <div class="persona-name">{persona_data["name"]}</div>
                </div>
            </div>
            <div class="persona-desc">{persona_data["desc"]}</div>
        </div>
        """
        st.markdown(persona_card_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="persona-card">
            <div style="text-align: center; color: #888; font-style: italic;">
                Please select a historical figure to begin your conversation.
            </div>
        </div>
        """, unsafe_allow_html=True)

# Section to ask question

st.markdown("### Ask your question:")

if st.session_state.selected_persona:
    persona_data = PERSONAS[st.session_state.selected_persona]
    question = st.text_area(
        "Your question",
        placeholder=persona_data["placeholder"],
        height=120,
        label_visibility="collapsed"
    )
    
    # Ask button
    if st.button("Ask Now", disabled=not question.strip()):
        if question.strip():
            # Show loading spinner
            with st.spinner(f"🎙️ Generating response and voice for {persona_data['name']}... This may take 1-2 minutes for high-quality audio generation."):
                try:
                    # API call
                    payload = {
                        "persona": st.session_state.selected_persona,
                        "question": question.strip()
                    }
                    
                    response = requests.post(
                        API_URL,
                        json=payload,
                        timeout=120,  
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Debug: Show what we received
                        st.success("✅ Response received successfully!")
                        
                        # Debug info 
                        with st.expander("🔍 Debug Info (Click to expand)"):
                            st.write("**API Response:**")
                            st.json(data)
                            if data.get('audio'):
                                st.write(f"**Audio Path from Backend:** `{data.get('audio')}`")
                                audio_path = data.get('audio')
                                if audio_path.startswith("static/"):
                                    st.write(f"**Expected File Location:** `{audio_path}`")
                                    st.write(f"**File Exists:** `{os.path.exists(audio_path)}`")
                                    if os.path.exists(audio_path):
                                        file_size = os.path.getsize(audio_path)
                                        st.write(f"**File Size:** `{file_size} bytes`")
                        
                        # Stored in conversation history
                        conversation_entry = {
                            "persona": st.session_state.selected_persona,
                            "question": question.strip(),
                            "answer": data.get('answer', 'No response received'),
                            "audio": data.get('audio', None)
                        }
                        st.session_state.conversation_history.append(conversation_entry)
                        
                        # To show the latest response
                        st.markdown("### 🎯 Latest Response:")
                        latest_response_html = f"""
                        <div class="response-card">
                            <div class="response-title">{persona_data["name"]} responds:</div>
                            <div style="color: #888; font-size: 0.9rem; margin-bottom: 10px;">
                                <strong>Your Question:</strong> {question.strip()}
                            </div>
                            <div class="response-text">{data.get('answer', 'No response received')}</div>
                        </div>
                        """
                        st.markdown(latest_response_html, unsafe_allow_html=True)
                        
                        # To show the audio immediately if available
                        if data.get('audio'):
                            audio_path = data.get('audio')
                            
                            # Handle TTS service audio path: static/{persona}_response.mp3
                            if audio_path.startswith("static/"):
                                audio_url = f"http://127.0.0.1:8000/{audio_path}"
                            elif not audio_path.startswith("http"):
                                if audio_path.startswith("/"):
                                    audio_url = f"http://127.0.0.1:8000{audio_path}"
                                else:
                                    audio_url = f"http://127.0.0.1:8000/{audio_path}"
                            else:
                                audio_url = audio_path
                            
                            st.write(f"🎵 **Audio Response from {persona_data['name']}:**")
                            
                            # Try multiple methods to play audio
                            try:
                                st.audio(audio_url, format='audio/mp3')
                                st.markdown(f"[⬇️ Download Audio]({audio_url})")
                            except Exception as audio_error:
                                st.warning(f"Primary audio method failed, trying alternative...")
                                # Alternative method: read file directly if it's local
                                if audio_path.startswith("static/") and os.path.exists(audio_path):
                                    try:
                                        with open(audio_path, 'rb') as audio_file:
                                            audio_bytes = audio_file.read()
                                            st.audio(audio_bytes, format='audio/mp3')
                                            st.success("✅ Audio loaded successfully!")
                                    except Exception as local_error:
                                        st.error(f"Could not load audio file: {local_error}")
                                else:
                                    st.error(f"Audio file not found at: {audio_path}")
                        else:
                            st.info("ℹ️ No audio was generated for this response.")
                        
                    else:
                        st.error(f"❌ Server Error: {response.status_code}")
                        st.error(f"Response: {response.text}")
                        
                except requests.exceptions.Timeout:
                    st.error("Request timed out after 2 minutes. The AI voice generation might be taking longer than expected. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the server. Please check if the backend is running.")
                except Exception as e:
                    st.error(f"Unexpected error occurred: {str(e)}")
else:
    st.text_area(
        "Your question",
        placeholder="Please select a historical figure first...",
        height=120,
        disabled=True,
        label_visibility="collapsed"
    )

# Display conversation history
if st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("### Recent Conversations:")
    
    # Show most recent conversation first
    for i, entry in enumerate(reversed(st.session_state.conversation_history[-3:])):  # Show last 3 conversations
        persona_data = PERSONAS[entry["persona"]]
        
        response_card_html = f"""
        <div class="response-card">
            <div class="response-title">{persona_data["name"]} responds:</div>
            <div style="color: #888; font-size: 0.9rem; margin-bottom: 10px;">
                <strong>Question:</strong> {entry["question"]}
            </div>
            <div class="response-text">{entry["answer"]}</div>
        </div>
        """
        st.markdown(response_card_html, unsafe_allow_html=True)
        
        # Audio player - Handle TTS generated audio files
        if entry["audio"]:
            try:
                audio_path = entry["audio"]
                
                # Handle the TTS service audio path format: static/{persona}_response.mp3
                if audio_path.startswith("static/"):
                    # Convert to proper URL for backend static files
                    audio_url = f"http://127.0.0.1:8000/{audio_path}"
                elif not audio_path.startswith("http"):
                
                    if audio_path.startswith("/"):
                        audio_url = f"http://127.0.0.1:8000{audio_path}"
                    else:
                        audio_url = f"http://127.0.0.1:8000/{audio_path}"
                else:
                    
                    audio_url = audio_path
                
                st.write(f"🎵 **Audio Response from {persona_data['name']}:**")
                
                # Try to load and display audio
                try:
                    st.audio(audio_url, format='audio/mp3')
                    st.markdown(f"[⬇️ Download Audio]({audio_url})")
                except Exception as audio_error:
                    st.warning(f"Could not load audio player. Trying alternative method...")
                    
                    if audio_path.startswith("static/") and os.path.exists(audio_path):
                        with open(audio_path, 'rb') as audio_file:
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format='audio/mp3')
                    else:
                        st.error(f"Audio file not accessible: {audio_url}")
                
            except Exception as e:
                st.warning(f"Audio playback error. Path: {entry.get('audio', 'None')} | Error: {str(e)}")
        else:
            st.info("ℹ️ No audio generated for this response.")

# Clear conversation button
if st.session_state.conversation_history:
    if st.button("Clear Conversation History"):
        st.session_state.conversation_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🎙️ Conversational Time Machine - Bringing history to life through AI</p>
    <p>Press Ctrl+R to refresh if you encounter any issues</p>
</div>
""", unsafe_allow_html=True)
