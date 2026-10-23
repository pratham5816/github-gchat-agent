from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router
from github_gchat_agent.agent.agent import get_agent, get_gemini_agent

  
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that runs on application startup and shutdown.
    Warms up and stores the Agents in app.state so they are always ready in memory.
    """
    try:
        app.state.agent = get_agent()
    except Exception as e:
        print(f"Failed to initialize Ollama agent: {e}")
        app.state.agent = None

    try:
        app.state.agent_gemini = get_gemini_agent()
    except Exception as e:
        print(f"Failed to initialize Gemini agent: {e}")
        app.state.agent_gemini = None

    yield

    print("Stopping GitHub GChat Agent server...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="GitHub GChat Agent API",
        description="FastAPI server with pre-warmed LangChain Agent for Google Chat & GitHub integration.",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    print("agent ready")
    return app


app = create_app()
