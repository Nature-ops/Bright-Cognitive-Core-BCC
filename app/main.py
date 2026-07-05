from fastapi import FastAPI
from app.models.chat import ChatRequest, ChatResponse

app = FastAPI(
    title="Bright Assistant",
    description="AI-powered Engineering Assistant",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Bright Assistant!",
        "version": "0.1.0",
        "status": "Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        response=f"Hello! You said: {request.message}"
    )
