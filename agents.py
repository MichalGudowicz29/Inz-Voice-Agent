from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain.agents.middleware import SummarizationMiddleware
from tools import get_geo_data, get_weather, search_web

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
import time


from langgraph.graph import StateGraph, START, END 
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from prompts import assistant_prompt
from pydantic import BaseModel, Field
from typing import Literal
from langchain_openai import ChatOpenAI
from voice import speak


class State(TypedDict):
    messages: Annotated[list, add_messages]
    action: Literal[
        "chat",
        "planner",
        "weather",
        "search",
        "calendar",
        "ask_user"
    ]

class AgentOutput(BaseModel):
    action: Literal[
        "chat",
        "planner",
        "weather",
        "search",
        "calendar",
        "ask_user"
    ] = Field(
        description="The next action the assistant should take"
    )

    answer: str = Field(
        description="Short spoken response for the user. Empty when another agent should handle the task."
    )

#potrzeba dodac allowed msgpack poniewaz langgraph ostrzega przed nieznanymi typami gdy agent chce wyciagnac cos z pamieci. 
checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(
        allowed_msgpack_modules=[
            ("prompts", "AgentOutput"),   # (nazwa modułu, nazwa klasy)
        ]
    )
)



# langchain agents
weather_agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    ),
    tools=[
        get_geo_data,
        get_weather
    ],
    system_prompt="""
    Jesteś agentem pogodowym.

    Twoim zadaniem jest odpowiedzieć użytkownikowi na pytania dotyczące pogody.

    Jeśli potrzebujesz lokalizacji:
    1. Pobierz współrzędne przez get_geo_data.
    2. Następnie użyj get_weather.

    Zawsze zwracaj krótką odpowiedź gotową do przeczytania przez TTS.
    """
)




llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
).with_structured_output(AgentOutput)


# node
# glowny asystent wejsciowy
def assistant_node(state: State):

    ct0 = time.time()
    
    response = llm.invoke([
        SystemMessage(content=assistant_prompt),
        *state["messages"]
    ])
    print(f"Conversation node: {time.time() - ct0:.3f}s")
    print(f"Action {response.action}")
    

    if response.action == "chat":
        speak(response.answer)


    return {
        "messages": [
            AIMessage(content=response.answer)
        ],
        "action": response.action
    }


# planner 
def planner_node(state: State):
    pt0 = time.time()
    plan = "Plan xyz"
    print(f"Planner ({time.time() - pt0:.3f}s)")
    return {'messages': [AIMessage(content=plan)]}


builder = StateGraph(State)
builder.add_node("assistant_node", assistant_node)
builder.add_node("planner", planner_node)

builder.add_edge(START, "assistant_node")
builder.add_conditional_edges(
    "assistant_node",
    lambda state: state["action"],
    {
        "chat": END,
        "planner": "planner"
    }
)

builder.add_edge("planner", END)

graph = builder.compile(checkpointer=checkpointer)

# Generowanie wizualizacji grafu
png = graph.get_graph().draw_mermaid_png()

with open("agent_graph.png", "wb") as f:
    f.write(png)

# Planner 

# Werfyikacja 

# Orkiestrator 


if __name__ == "__main__":
    png = graph.get_graph().draw_mermaid_png()

    with open("agent_graph.png", "wb") as f:
        f.write(png)
