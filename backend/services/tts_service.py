import requests
import os
import uuid
from collections import defaultdict, deque

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_IDS = {
    "indira": os.getenv("INDIRA_VOICE_ID"),
    "atal": os.getenv("ATAL_VOICE_ID")
}


AUDIO_HISTORY = defaultdict(lambda: deque(maxlen=5))
AUDIO_DIR = "static"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_voice(text: str, persona: str) -> str:
    voice_id = VOICE_IDS.get(persona.lower())
    if not voice_id:
        raise ValueError(f"No voice ID configured for persona: {persona}")
    
    # Calling the ElevenLabs API
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {"stability": 0.7, "similarity_boost": 0.8}
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"TTS failed: {response.text}")
    
    # Generating a unique file name for new audio
    file_name = f"{persona}_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(AUDIO_DIR, file_name)
    
    
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    
    AUDIO_HISTORY[persona].append(file_name)

    return f"static/{file_name}"
