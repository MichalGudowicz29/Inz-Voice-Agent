from dotenv import load_dotenv
import uuid
load_dotenv()

#langchain graph 
from langchain.messages import HumanMessage
from langgraph.types import Command

from voice.tts import speak

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

#static 
#listener = ["Czesc podasz mi pogode w Szczecinie", "Super powiedz mi jaka jest temperatura obecnie"]

for message, delay, reason in listener:

    if reason:
        print(f"asr fail: reason '{reason}'")
        speak("Nie zrozumiałem. Czy możesz powtórzyć?")
        continue

    ot0 = time.time()
    print(f"Ty: {message}") 
    print(f"ASR delay: {delay:.2f}s")


    result = graph.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=chat_config
    ) 

    if "__interrupt__" in result:

        question = result["__interrupt__"][0].value
        speak(question)

        answer, delay, reason = next(listener)

        while reason:
            print(f"asr fail: reason '{reason}'")
            speak("Nie zrozumiałem. Czy możesz powtórzyć?")
            answer, delay, reason = next(listener)

        result = graph.invoke(
            Command(resume=answer),
            config=chat_config
        )

    ot1 = time.time()
    overall_time = ot1-ot0

    
    print("Chat: " + result['messages'][-1].content)
    print(f"Overall time: {overall_time} s")
    
