# 🎙️ Conversational Time Machine

Conversational Time Machine is an **AI-powered interactive application** that allows you to **chat with historical leaders** and listen to their **realistic AI-generated voice responses**.
Currently, the application features **two personas**:
- **Indira Gandhi** (First female Prime Minister of India)
- **Atal Bihari Vajpayee** (Former Prime Minister of India)

---

# 🌐 Live Demo
🔗 Try the app now: [web-production-d013b.up.railway.app](web-production-d013b.up.railway.app)

The app is deployed on Railway and ready to use! Simply select a historical figure and start asking questions.

---

## 🚀 Features
- **Chat with Historical Figures:** Ask questions and get contextually accurate responses.
- **Voice Responses:** AI-generated voices using **ElevenLabs TTS** for each persona.
- **Conversation History:** Displays the **last 3 questions and answers** with voice playback.
- **RAG (Retrieval-Augmented Generation):** Uses **FAISS** and **Groq’s LLaMA 3.3 model** for persona-based answers.
- **Modern UI:** Beautiful interface built with **Streamlit**.
- **FastAPI Backend:** Manages AI response generation and voice synthesis.

---

## 🛠 Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **AI Model:** Groq (LLaMA 3.3 70B)
- **Embeddings & Search:** FAISS Vector Store
- **Text-to-Speech:** ElevenLabs API
- **Language:** Python 3.9+

---

## 📂 Project Structure
```yaml

```
.
├── backend/
│   ├── data/
│   │   ├── faiss_atal/
│   │   │   ├── index.faiss
│   │   │   └── index.pkl
│   │   ├── faiss_indira/
│   │   │   ├── index.faiss
│   │   │   └── index.pkl
│   │   ├── Atal_Bihari_Vajpayee.pdf
│   │   ├── Indira_Gandhi.pdf
│   │   ├── atal_g_quotes.txt
│   │   ├── atal_g_speeches.txt
│   │   ├── quotes.txt
│   │   └── speeches.txt
│   ├── routes/
│   │   ├── __init__.py
│   │   └── conversation.py         # Chat API routes
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prepare_embeddings.py
│   │   ├── rag_service.py        # For RAG
│   │   └── tts_service.py        # ElevenLabs TTS service
│   ├── static/                   # Generated audio files
│   │   ├── atal_39e36c77e34a45b0b3f463... (audio files)
│   │   ├── atal_b871bb8165f74af0b7c1f7...
│   │   ├── atal_e72c6c4e0db840d68bb25...
│   │   ├── atal_response.mp3
│   │   ├── indira_733a7532e05b46dcbcf9... (audio files)
│   │   ├── indira_b45ee83ad9a7481f9afd...
│   │   ├── indira_ca28fd99bf0543498475...
│   │   ├── indira_d8342c1ba4fe44388699...
│   │   └── indira_response.mp3
│   ├── main.py                      # FastAPI backend entry point
│   └── requirements.txt
├── frontend/
│   ├── assets/                       # Persona images
│   ├── app.py
│   └── requirements.txt
├── utils/
│   ├── prompt_templates.py 
│   ├── vector_store.py           # FAISS vector loading
│   └── audio_history.json
├── Procfile
├── README.md
├── .gitattributes
├── .gitignore
├── debug.py            # For debugging 
└── debug2.py
```
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)jatin019/Conversational-Time-Machine-Project.git
cd conversational-time-machine
```
### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a `.env` file in the root directory and add:
```ini
GROQ_API_KEY=your_groq_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
INDIRA_VOICE_ID=your_indira_voice_id
ATAL_VOICE_ID=your_atal_voice_id
```
### 5. Run the Backend (FastAPI)
```bash
uvicorn main:app --reload
```
### 6. Run the Frontend (Streamlit)
```bash
streamlit run app.py
```

---

## 🌐 Deployment
You can deploy:
- Backend on Render (FastAPI + static audio hosting)
- Frontend on Streamlit Community Cloud

---

## 🖼 Preview
- Chat with Indira Gandhi or Atal Bihari Vajpayee
- Listen to their voice responses
- View conversation history (last 3 Q&A pairs)

---

## 🤝 Contributing
Pull requests and suggestions are welcome.
For major changes, open an issue first to discuss what you’d like to improve.

---

## 📜 License
This project is licensed under the MIT License.

---

## ✨ Credits
- LLaMA 3.3 70B – via Groq API
- ElevenLabs – for AI voice generation
- Streamlit & FastAPI – for frontend and backend
