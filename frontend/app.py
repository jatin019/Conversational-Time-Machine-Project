import gradio as gr
import requests
import json
import base64
import os
from typing import Optional, Tuple, List


# Function to get base64 image
def get_base64_image(path: str) -> Optional[str]:
    """Convert image to base64 string"""
    try:
        with open(path, "rb") as img_file:
            return f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode()}"
    except FileNotFoundError:
        return None

# Load images
indira_img = get_base64_image("assets/indira gandhi.jpg")
atal_img = get_base64_image("assets/atal bihari vajpayee.jpeg")

# API configuration
API_URL = "http://127.0.0.1:8000/api/chat/"

# Persona data
PERSONAS = {
    "indira": {
        "name": "Indira Gandhi",
        "desc": "First female Prime Minister of India (1966–1984). Known for decisive leadership and her role in shaping modern India.",
        "image": "assets/indira gandhi.jpg" if os.path.exists("assets/indira gandhi.jpg") else None,
        "placeholder": "e.g., What was your role in the Bangladesh Liberation War?"
    },
    "atal": {
        "name": "Atal Bihari Vajpayee", 
        "desc": "Former Prime Minister (1998–2004), statesman, poet, and visionary leader known for his oratory skills.",
        "image": "assets/atal bihari vajpayee.jpeg" if os.path.exists("assets/atal bihari vajpayee.jpeg") else None,
        "placeholder": "e.g., What inspired your poetry and political philosophy?"
    }
}

# Global conversation history
conversation_history = []

def get_persona_info(persona_key: str) -> str:
    """Get persona information as HTML"""
    if not persona_key or persona_key == "Select a leader...":
        return "<div style='text-align: center; color: #888; font-style: italic; padding: 20px;'>Please select a historical figure to begin your conversation.</div>"
    
    persona = PERSONAS.get(persona_key)
    if not persona:
        return "<div style='color: #f44336;'>Persona not found</div>"
    
    image_html = ""
    if persona["image"] and os.path.exists(persona["image"]):
        image_html = f'<img src="file/{persona["image"]}" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; margin-right: 20px; border: 3px solid #4ecdc4;" />'
    
    return f"""
    <div style="background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            {image_html}
            <div>
                <h3 style="color: #ffffff; margin: 0 0 5px 0; font-size: 1.4rem;">{persona["name"]}</h3>
                <p style="color: #b0b0b0; margin: 0; line-height: 1.6;">{persona["desc"]}</p>
            </div>
        </div>
    </div>
    """

def update_placeholder(persona_key: str) -> str:
    """Update placeholder text based on selected persona"""
    if not persona_key or persona_key == "Select a leader...":
        return "Please select a historical figure first..."
    
    persona = PERSONAS.get(persona_key)
    return persona["placeholder"] if persona else "Enter your question..."

def chat_with_persona(persona_key: str, question: str, history: List) -> Tuple[List, str, str]:
    """Chat with selected persona and return updated history, audio, and status"""
    global conversation_history
    
    if not persona_key or persona_key == "Select a leader...":
        return history, None, "❌ Please select a historical figure first."
    
    if not question.strip():
        return history, None, "❌ Please enter a question."
    
    persona = PERSONAS.get(persona_key)
    if not persona:
        return history, None, "❌ Invalid persona selected."
    
    try:
        # Show loading status
        status = f"🎙️ Generating response and voice for {persona['name']}... This may take 1-2 minutes for high-quality audio generation."
        
        # API call
        payload = {
            "persona": persona_key,
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
            
            # Create conversation entry
            conversation_entry = {
                "persona": persona_key,
                "persona_name": persona["name"],
                "question": question.strip(),
                "answer": data.get('answer', 'No response received'),
                "audio": data.get('audio', None)
            }
            
            # Add to global history
            conversation_history.append(conversation_entry)
            
            # Update chat history for display
            new_history = history + [[f"🙋 **You asked {persona['name']}:** {question}", f"🎭 **{persona['name']} responds:**\n\n{data.get('answer', 'No response received')}"]]
            
            # Handle audio
            audio_path = None
            if data.get('audio'):
                audio_file_path = data.get('audio')
                
                # Convert backend path to accessible path
                if audio_file_path.startswith("static/"):
                    # For TTS generated files
                    if os.path.exists(audio_file_path):
                        audio_path = audio_file_path
                    else:
                        # Try alternative paths
                        alt_path = audio_file_path.replace("static/", "")
                        if os.path.exists(alt_path):
                            audio_path = alt_path
                
            return new_history, audio_path, f"✅ Response received successfully from {persona['name']}!"
            
        else:
            return history, None, f"❌ Server Error: {response.status_code} - {response.text}"
            
    except requests.exceptions.Timeout:
        return history, None, "❌ Request timed out after 2 minutes. Please try again."
    except requests.exceptions.ConnectionError:
        return history, None, "❌ Unable to connect to the server. Please check if the backend is running."
    except Exception as e:
        return history, None, f"❌ Unexpected error: {str(e)}"

def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return [], None, "🧹 Conversation history cleared!"

# Custom CSS for dark theme
custom_css = """
/* Dark theme styling */
.gradio-container {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%) !important;
    color: #ffffff !important;
}

.gr-button-primary {
    background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%) !important;
    border: none !important;
    border-radius: 25px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.gr-button-primary:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4) !important;
}

.gr-textbox, .gr-dropdown {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
}

.gr-chatbot {
    background-color: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 15px !important;
}

/* Custom styling for chat messages */
.gr-chatbot .message {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
}

.gr-audio {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 15px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}
"""

# Create Gradio interface
with gr.Blocks(
    title="🎙️ Conversational Time Machine",
    theme=gr.themes.Base().set(
        background_fill_primary="#0a0a0a",
        background_fill_secondary="#1a1a2e",
        block_background_fill="#16213e",
        input_background_fill="rgba(255, 255, 255, 0.05)",
        button_primary_background_fill="linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%)"
    ),
    css=custom_css
) as app:
    
    # Header
    gr.HTML("""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;">
            🎙️ Conversational Time Machine
        </h1>
        <p style="font-size: 1.2rem; color: #b0b0b0; font-weight: 300;">
            Chat with historical leaders and hear their voice in real-time!
        </p>
    </div>
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            # Persona selection
            gr.HTML("<h3 style='color: #ffffff; margin-bottom: 15px;'>Choose a historical figure:</h3>")
            persona_dropdown = gr.Dropdown(
                choices=["Select a leader..."] + [PERSONAS[key]["name"] for key in PERSONAS.keys()],
                value="Select a leader...",
                label="Historical Figure",
                interactive=True
            )
            
            # Convert dropdown selection to persona key
            def get_persona_key(selection):
                if selection == "Select a leader...":
                    return "Select a leader..."
                for key, data in PERSONAS.items():
                    if data["name"] == selection:
                        return key
                return "Select a leader..."
        
        with gr.Column(scale=2):
            # Persona info display
            persona_info = gr.HTML(
                value=get_persona_info(""),
                label="Selected Leader Info"
            )
    
    # Question input section
    gr.HTML("<h3 style='color: #ffffff; margin: 30px 0 15px 0;'>Ask your question:</h3>")
    
    with gr.Row():
        with gr.Column(scale=4):
            question_input = gr.Textbox(
                placeholder="Please select a historical figure first...",
                lines=3,
                label="Your Question",
                interactive=True
            )
        with gr.Column(scale=1):
            ask_button = gr.Button(
                "Ask Now",
                variant="primary",
                size="lg"
            )
    
    # Status display
    status_display = gr.HTML(
        value="<div style='color: #888; font-style: italic;'>Select a leader and ask a question to begin.</div>",
        label="Status"
    )
    
    # Chat history
    chatbot = gr.Chatbot(
        value=[],
        height=400,
        label="Conversation History",
        show_label=True,
        container=True,
        scale=1
    )
    
    # Audio output
    audio_output = gr.Audio(
        label="🎵 Audio Response",
        visible=True,
        interactive=False
    )
    
    # Clear button
    with gr.Row():
        clear_button = gr.Button(
            "Clear Conversation History",
            variant="secondary"
        )
    
    # Debug info (collapsible)
    with gr.Accordion("🔍 Debug Info", open=False):
        debug_info = gr.JSON(
            value={},
            label="API Response Data"
        )
    
    # Event handlers
    def update_ui_on_persona_change(selection):
        persona_key = get_persona_key(selection)
        persona_html = get_persona_info(persona_key)
        placeholder = update_placeholder(persona_key)
        return persona_html, gr.update(placeholder=placeholder)
    
    def handle_chat(persona_selection, question, history):
        persona_key = get_persona_key(persona_selection)
        new_history, audio_path, status = chat_with_persona(persona_key, question, history)
        
        # Clear the question input
        return new_history, audio_path, status, ""
    
    # Wire up events
    persona_dropdown.change(
        fn=update_ui_on_persona_change,
        inputs=[persona_dropdown],
        outputs=[persona_info, question_input]
    )
    
    ask_button.click(
        fn=handle_chat,
        inputs=[persona_dropdown, question_input, chatbot],
        outputs=[chatbot, audio_output, status_display, question_input]
    )
    
    question_input.submit(
        fn=handle_chat,
        inputs=[persona_dropdown, question_input, chatbot],
        outputs=[chatbot, audio_output, status_display, question_input]
    )
    
    clear_button.click(
        fn=clear_history,
        outputs=[chatbot, audio_output, status_display]
    )

# Launch the app
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True,
        show_error=True
    )