from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import planner_prompt
from pydantic import BaseModel, Field 
from typing import Optional

load_dotenv()


class PlanOutput(BaseModel):
    task: str = Field(description="Oryginalne zadanie od uzytkownika, czego oczekuje od systemu. Jaki jest main task")
    needs_clarification: bool = Field(
        description="True tylko jeśli bez doprecyzowania od użytkownika nie da się "
                    "zbudować wykonalnego planu. False jeśli masz wystarczająco informacji."
    )
    clarification_question: Optional[str] = Field(
        default=None,
        description="Krótkie, konkretne pytanie do użytkownika. Ustawiane TYLKO gdy "
                    "needs_clarification=True. Jedno pytanie, nie lista pytań."
    )
    description: str = Field(
        description="Krótki opis celu planu (1 zdanie). Puste jeśli needs_clarification=True."
    )
    steps: list[str] = Field(
        default_factory=list,
        description="Uporządkowana lista kroków dla agenta-egzekutora. Pusta lista "
                    "jeśli needs_clarification=True."
    )
    number_of_steps: int = Field(
            description="How many steps does plan has"
    )


llm = ChatOpenAI(
    model="gpt-4o-mini"
).with_structured_output(PlanOutput)


def planner_agent(messages, success, reason):

    system_prompt = planner_prompt

    if not success:
        system_prompt += (
            f"\n\nThe previous execution failed.\n"
            f"Reason: {reason}\n"
            "Create a new improved plan that avoids this failure."
        )

    return llm.invoke([
        {"role": "system", "content": system_prompt},
        *messages,
    ])
