from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts import planner_prompt
from pydantic import BaseModel

load_dotenv()


class PlanOutput(BaseModel):

    steps:list[str]


llm = ChatOpenAI(
    model="gpt-4o-mini"
).with_structured_output(PlanOutput)


def planner_agent(user_request):

    result = llm.invoke(
        [
            {
                "role":"system",
                "content":planner_prompt
            },
            {
                "role":"user",
                "content":user_request
            }
        ]
    )

    return result
