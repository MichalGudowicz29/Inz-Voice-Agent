from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain.agents.middleware import SummarizationMiddleware
from tools import get_geo_data, get_weather, search_web
from voice import init_transcribe_model, listen, speak
checkpointer = InMemorySaver()



# Router
router = agent.create_agent()



# Konwersacja

# Planner 

# Werfyikacja 

# Orkiestrator 



