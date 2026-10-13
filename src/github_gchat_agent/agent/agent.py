from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from github_gchat_agent.tools.agent_tools import get_issues, get_open_pullrequests , send_message_google_chat
import json

  

class AgentResponse(BaseModel):
    message: str
    passed: bool

def get_agent():

    model = ChatOllama(
        model="qwen3:4b",
        temperature=0,
    )

    system_prompt="""
    You are a fast assistant.

    Use tools when needed.
    Do not overthink.

    Always return a structured response containing:
    - message: your response to the user
    - passed: true if you successfully handled the request, otherwise false
    """

    agent = create_agent(
        model=model,
        tools=[get_issues,get_open_pullrequests,send_message_google_chat],
        system_prompt=system_prompt,
        response_format=AgentResponse
    )
    print("agent ready")
    return agent if agent and model else Exception 


def invoke_agent(agent: object , prompt: str , role: str):
    response = agent.invoke({
    "messages": [
        {
            "role": role,
            "content": prompt,
        }
    ]
    })

    return response if response  else "Sorry try again later..."
   
