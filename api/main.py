from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent.agent_llm_handler import run_agent_chain

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def index():
    return {"message": "Chat API is running."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_query = request.query
    response = await run_agent_chain(user_query)
    return {"response": response}
