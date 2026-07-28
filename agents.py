from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain.agents.middleware import SummarizationMiddleware
from tools import get_geo_data, get_weather, search_web

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer


#potrzeba dodac allowed msgpack poniewaz langgraph ostrzega przed nieznanymi typami gdy agent chce wyciagnac cos z pamieci. 
checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(
        allowed_msgpack_modules=[
            ("prompts", "RouterOutput"),   # (nazwa modułu, nazwa klasy)
        ]
    )
)


from prompts import router_prompt, RouterOutput, conversational_prompt

# Router
router_agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather, get_geo_data, search_web],
    system_prompt=router_prompt,
    response_format=RouterOutput, 
    checkpointer=checkpointer,
)



# Konwersacja
conversational_agent = create_agent(
    model="gpt-5-nano",
    system_prompt=conversational_prompt,
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model='gpt-5-nano',
            trigger=('messages', 20), 
            keep=('messages', 5)
        )
    ]
)

# Planner 

# Werfyikacja 

# Orkiestrator 



