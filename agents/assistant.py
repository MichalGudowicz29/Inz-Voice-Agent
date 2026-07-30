from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import assistant_prompt
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()


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



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
).with_structured_output(AgentOutput)


def assistant_agent(messages):

    response = llm.invoke(
        [
            {
                "role":"system",
                "content":assistant_prompt
            },
            *messages
        ]
    )

    return response
