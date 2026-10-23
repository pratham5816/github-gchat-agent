"""
FastAPI Routes handling health checks and Agent chat requests.
"""
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from github_gchat_agent.agent.agent import invoke_agent

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    model: str = "ollama"  # "ollama" or "gemini"


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "github-gchat-agent"}


@router.post("/agent/ollama/chat")
async def handle_ollama_chat(body: ChatRequest, request: Request) -> Dict[str, Any]:
    """
    Dedicated endpoint for the Ollama agent.
    """
    agent = getattr(request.app.state, "agent", None)
    if not agent:
        raise HTTPException(status_code=500, detail="Ollama agent not ready or not initialized")

    try:
        response = invoke_agent(agent=agent, prompt=body.prompt, role="user")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing Ollama agent: {str(e)}")


@router.post("/agent/gemini/chat")
async def handle_gemini_chat(body: ChatRequest, request: Request) -> Dict[str, Any]:
    """
    Dedicated endpoint for the Gemini agent.
    """
    agent = getattr(request.app.state, "agent_gemini", None)
    if not agent:
        raise HTTPException(status_code=500, detail="Gemini agent not ready or not initialized")

    try:
        response = invoke_agent(agent=agent, prompt=body.prompt, role="user")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing Gemini agent: {str(e)}")


@router.post("/agent/chat")
async def handle_agent_chat(body: ChatRequest, request: Request) -> Dict[str, Any]:
    """
    Unified endpoint receiving {"prompt": "...", "model": "ollama"|"gemini"}.
    Defaults to Ollama.
    """
    if body.model.lower() == "gemini":
        return await handle_gemini_chat(body, request)
    return await handle_ollama_chat(body, request)