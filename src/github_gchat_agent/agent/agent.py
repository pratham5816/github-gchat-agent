from langchain.agents import create_agent
from langchain.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from github_gchat_agent.tools.github_tools import get_issues, get_open_pullrequests
import json

  

class AgentResponse(BaseModel):
    message: str
    passed: bool

def get_agent():

    model = ChatOllama(
        model="qwen3:4b",
        temperature=0,
    )

    system_prompt="""You are a fast assistant.
                     Use tools when needed.
                     Do not overthink."""

    agent = create_agent(
        model=model,
        tools=[get_issues,get_open_pullrequests],
        system_prompt=system_prompt,
        response_format=AgentResponse
    )

    return agent



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
   
