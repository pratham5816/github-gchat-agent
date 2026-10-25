from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from github_gchat_agent.tools.agent_tools import get_issues, get_open_pullrequests , send_message_google_chat
import json , os
from dotenv import load_dotenv

  

class AgentResponse(BaseModel):
    message: str
    passed: bool

def get_agent():
    model = ChatOllama(
        model="llama3.2:3b",
        temperature=0,
    )

    system_prompt = """
    You are a fast assistant.

    Use tools when needed.
    Do not overthink.
    """

    agent = create_agent(
        model=model,
        tools=[get_issues, get_open_pullrequests, send_message_google_chat],
        system_prompt=system_prompt,
        response_format=AgentResponse,
    )
    print("Ollama agent ready")
    if not (agent and model):
        raise RuntimeError("Failed to initialize Ollama agent")
    return agent


def get_gemini_agent():
    load_dotenv()
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key

    system_prompt = """
    You are a fast assistant.

    Use tools when needed.
    Do not overthink.
    """

    agent = create_agent(
        model="google_genai:gemini-3.5-flash-lite",
        tools=[get_issues, get_open_pullrequests, send_message_google_chat],
        system_prompt=system_prompt,
        response_format=AgentResponse,
    )
    print("Gemini agent ready")
    if not agent:
        raise RuntimeError("Failed to initialize Gemini agent")
    return agent


def invoke_agent(agent: object, prompt: str, role: str):
    response = agent.invoke({
        "messages": [
            {
                "role": role,
                "content": prompt,
            }
        ]
    })

    if not response:
        return {"message": "Sorry try again later...", "passed": False}

    content = response["messages"][-1].content
    # When content is a list of blocks (as in some Google GenAI responses), extract text
    if isinstance(content, list) and len(content) > 0:
        if isinstance(content[0], dict) and "text" in content[0]:
            content = content[0]["text"]
        elif hasattr(content[0], "text"):
            content = content[0].text

    try:
        return json.loads(content)
    except (json.JSONDecodeError, TypeError):
        return {"message": content, "passed": True}



