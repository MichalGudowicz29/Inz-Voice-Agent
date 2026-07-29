from dotenv import load_dotenv
load_dotenv()

#langchain graph 
from langchain.messages import HumanMessage
import time

from voice import light_listen
from agents import graph


chat_config = {
    "configurable": {
        "thread_id": "conversation"
    }
}

listener = light_listen()

for message in listener:

    if not message:
        continue
    
    ot0 = time.time()
    print(f"Ty: {message}") 

    result = graph.invoke(
        {"messages": [HumanMessage(message)]},
        config=chat_config
    ) 
    ot1 = time.time()
    overall_time = ot1-ot0

    
    print("Chat: " + result['messages'][-1].content)
    print(f"Overall time: {overall_time} s")
    

