#env imports
from dotenv import load_dotenv
load_dotenv()

#langchain graph 
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain.agents.middleware import SummarizationMiddleware

#additional
import time

# local imports
from tools import get_geo_data, get_weather, search_web
from voice import light_listen, speak
from agents import router_agent, conversational_agent


config = {'configurable': {'thread_id':'1'}}
listener=light_listen()

for message in listener:

    if not message:
        continue

    print("=" * 10)
    print(f"Ty: {message}") 
    print("=" * 10)
    # rt stands for response time
    rt0 = time.time() 
    response = router_agent.invoke(
        {"messages": HumanMessage(content=message)},
        config=config
    )
    rt1 = time.time()
    router_invoke = rt1-rt0

    
    print(f"Router decision: {response["structured_response"].need_plan}")
    if response['structured_response'].need_plan:
        #call planer
        continue
    else:
        #call conversational
        ct0 = time.time()
        answer = conversational_agent.invoke(
            {"messages": HumanMessage(content=message)},
            config=config
        )
        ct1 = time.time()
        conversational_invoke = ct1 - ct0
        
        


    # for msg in response['messages']:
    #     msg.pretty_print()
    # print("-" * 10)
    # print("Ilosc wiadomosci w pamieci: " + str(len(response['messages'])))
    # print("-" * 10)
    print("Chat: " + answer['messages'][-1].content)
    print(f"ri: {router_invoke} s")
    print(f"ci: {conversational_invoke} s")

