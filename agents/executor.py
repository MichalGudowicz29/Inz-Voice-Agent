from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts.executor_prompt import executor_prompt
from agents.tool_agents import call_search_agent, call_weather_agent  
from langchain.agents import create_agent

from pydantic import BaseModel, Field 
from typing import Optional

load_dotenv()



class ExecutorOutput(BaseModel):
    success: bool = Field(
        description="Whether the entire execution completed successfully."
    )

    final_answer: str = Field(
        description="Answer that should be shown to the user."
    )

    failed_step: Optional[int] = Field(
        default=None,
        description="Index of the step that failed."
    )

    failure_reason: Optional[str] = Field(
        default=None,
        description="Why execution could not continue."
    )

    completed_steps: int = Field(
        description="Number of successfully completed steps."
    )
        


exec_agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ),
    tools=[
        call_weather_agent,
        call_search_agent
    ],
    system_prompt=executor_prompt,
    response_format=ExecutorOutput
) 


def executor_agent(task: str, plan: list[str]):
    query = f"""Task:
        {task}

        Execute the following plan exactly as written:

        {chr(10).join(f"{i + 1}. {step}" for i, step in enumerate(plan))}
    """
    
    return exec_agent.invoke({
        'messages': [
            {'role':'user', 'content': query}
        ]},    
    )    

