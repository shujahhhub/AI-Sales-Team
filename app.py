from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn

# 1. Initialize the FastAPI application
app = FastAPI(
    title="AI Chatbot Microservice",
    description="A containerized FastAPI backend serving a Hugging Face LLM.",
    version="1.0.0"
)

# 2. Load the Open-Source LLM into memory
# We are using Blenderbot, a lightweight model specifically trained for conversational chat.
print("Downloading and loading the AI model... (This may take a minute the first time)")
try:
    chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# 3. Define the Data Models (Pydantic)
# This ensures our API strictly validates the incoming and outgoing data.
class ChatRequest(BaseModel):
    user_message: str

class ChatResponse(BaseModel):
    ai_response: str

# 4. Create the Health Check Endpoint
# Kubernetes will use this endpoint to check if the pod is alive and healthy.
@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "facebook/blenderbot-400M-distill"}

# 5. Create the Core AI Chat Endpoint
@app.post("/chat", response_model=ChatResponse)
def chat_with_ai(request: ChatRequest):
    if not request.user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        # Feed the user's message to the AI
        conversation = chatbot(request.user_message)
        
        # Extract the AI's generated response
        # The pipeline returns a Conversation object; we grab the last generated response.
        reply = conversation.generated_responses[-1]
        
        return ChatResponse(ai_response=reply)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

# 6. Local Testing Execution
if __name__ == "__main__":
    # Runs the server locally on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)