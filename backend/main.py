from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from backend.routes.conversation import router as conversation_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Conversational Time Machine")
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conversation_router, prefix="/api/chat")

@app.get("/")
def root():
    return {"message": "Conversational Time Machine API is running"}
