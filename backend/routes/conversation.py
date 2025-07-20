from fastapi import APIRouter
from pydantic import BaseModel
from services.rag_service import get_persona_response
from services.tts_service import generate_voice

router = APIRouter()

class ChatRequest(BaseModel):
    persona: str
    question: str

@router.post("/")
async def chat(req: ChatRequest):
    response_text = get_persona_response(req.persona, req.question)
    audio_file = generate_voice(response_text, req.persona)
    return {"answer": response_text, "audio": audio_file}
