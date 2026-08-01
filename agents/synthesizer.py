from prompts import synthesizer_prompt
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompts.executor_prompt import executor_prompt
from agents.tool_agents import call_search_agent, call_weather_agent  
from langchain.agents import create_agent

from pydantic import BaseModel, Field 
from typing import Optional

load_dotenv()



class SynthesizerOutput(BaseModel):
    spoken_response: str = Field(
        description="Natural language ready for TTS module to be spoken text. Optionally offering ONE relevant follow-up question."
    )


synthesizer = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ),
    system_prompt=synthesizer_prompt,
    response_format=SynthesizerOutput
) 


def synthesizer_agent(task: str, final_answer: str):
    query = f"Task: {task}\nFinal answer (raw): {final_answer}" 
    return synthesizer.invoke({
        'messages': [
            {'role':'user', 'content': query}
        ]},    
    )    






