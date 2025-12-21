from fastapi import APIRouter
from pydantic import BaseModel
from qa import QASystem

router = APIRouter()
qa_system = QASystem()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    reply = qa_system.answer(req.message)
    return {"reply": reply}
