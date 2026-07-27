from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain.agents.middleware import SummarizationMiddleware
from tools import get_geo_data, get_weather, search_web
from voice import init_transcribe_model, listen, speak
checkpointer = InMemorySaver()


agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather, get_geo_data, search_web],
    system_prompt="You are a helpful assistant, very bad at guessing but you have a lot of tools you can use that will provide you real time information, so instead of guessing you should always check if there is possible tool to use to acomplishe task, then call it and us it.",
    checkpointer=checkpointer,
    middleware=[
        SummarizationMiddleware(
            model='gpt-5-nano',
            trigger=('messages', 20), 
            keep=('messages', 5)
        )
    ]
)
config = {'configurable': {'thread_id':'1'}}



while True:
    message = str(input("Ty: "))

    # Run the agent
    response = agent.invoke(
        {"messages": message},
        config=config
    )
   # for msg in response['messages']:
   #     msg.pretty_print()
   # print("-" * 10)
   # print("Ilosc wiadomosci w pamieci: " + str(len(response['messages'])))
   # print("-" * 10)
    print("=" * 10)
    print("Chat: " + response['messages'][-1].content)
    print("=" * 10)

