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


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "ok", "service": "github-gchat-agent"}


@router.post("/agent/chat")
async def handle_agent_chat(body: ChatRequest, request: Request) -> Dict[str, Any]:
    """
    Endpoint receiving {"prompt": "..."} and passing it to the pre-warmed Agent.
    """
    agent = getattr(request.app.state, "agent", None)
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not ready or not initialized")

    try:
        response = invoke_agent(agent=agent, prompt=body.prompt, role="user")
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing agent: {str(e)}")