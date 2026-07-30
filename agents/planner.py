from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import planner_prompt
from pydantic import BaseModel, Field, Optional

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


llm = ChatOpenAI(
    model="gpt-5-nano"
).with_structured_output(PlanOutput)


def planner_agent(messages):

    return llm.invoke(
        [
            {
                "role": "system",
                "content": planner_prompt,
            },
            *messages,
        ]
    )
