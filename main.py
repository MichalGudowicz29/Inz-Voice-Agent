from dotenv import load_dotenv
import uuid
load_dotenv()

#langchain graph 
from langchain.messages import HumanMessage
import time

from graph import graph
from voice.asr import listen


chat_config = {
    "configurable": {
        "thread_id": uuid.uuid4()
    }
}

listener = listen()
#listener = light_listen()

for message,delay in listener:

    if not message:
        continue
    
    ot0 = time.time()
    print(f"Ty: {message}") 
    print(f"ASR delay: {delay:.2f}s")


    result = graph.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=chat_config
    ) 
    ot1 = time.time()
    overall_time = ot1-ot0

    
    print("Chat: " + result['messages'][-1].content)
    print(f"Overall time: {overall_time} s")
    
