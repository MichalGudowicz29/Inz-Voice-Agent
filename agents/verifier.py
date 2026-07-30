from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import planner_prompt
from pydantic import BaseModel, Field, Optional

load_dotenv()


class VerifierOutput(BaseModel):
    verified: bool = Field(description="Is the plan able to accomplish with given tools, and if it accomplish task granted by user") 



llm = ChatOpenAI(
    model="gpt-5-nano"
).with_structured_output(VerifierOutput)


def verification_agent(messages):

    return llm.invoke(
        [
            {
                "role": "system",
                "content": verification_prompt,
            },
            *messages,
        ]
    )

