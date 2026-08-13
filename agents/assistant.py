from dotenv import load_dotenv
from prompts import assistant_prompt
from pydantic import BaseModel, Field
from typing import Literal
from langchain.messages import SystemMessage
from langchain_ollama import ChatOllama



load_dotenv()

LIGHT_MODEL = 'hf.co/SpeakLeash/Bielik-4.5B-v3.0-Instruct-GGUF:Q8_0'
HEAVY_MODEL = 'SpeakLeash/bielik-11b-v3.0-instruct:Q4_K_M'



class AgentOutput(BaseModel):
    action: Literal[
        "chat",
        "planner",
    ] = Field(
        description="The next action the assistant should take"
    )

    answer: str = Field(
        description="Short spoken response for the user. Empty when another agent should handle the task."
    )


llm = ChatOllama(model=LIGHT_MODEL).with_structured_output(AgentOutput) 

def assistant_agent(messages):
    response = llm.invoke([
        SystemMessage(content=assistant_prompt),
        *messages,
    ])

    return response
