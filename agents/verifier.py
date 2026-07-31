from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import verification_prompt
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

class VerificationOutput(BaseModel):
    verified: bool = Field(
        description="True only if the plan passes all four checks with no exceptions."
    )
    reasoning: str = Field(
        description="Specific explanation of which check failed and why, or why "
                    "the plan passed all checks. Must be specific enough for the "
                    "Planner to fix the plan without guessing."
    )



llm = ChatOpenAI(
    model="gpt-4o-mini"
).with_structured_output(VerificationOutput)


def verification_agent(task: str, plan: list[str]):
    plan_text = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))

    return llm.invoke(
        [
            {"role": "system","content": verification_prompt},
            {
                "role": "user",
                "content": f"Task: {task}, Plan: {plan}"
            },
        ]
    )

