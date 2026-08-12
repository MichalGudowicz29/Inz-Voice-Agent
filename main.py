from dotenv import load_dotenv
import uuid
load_dotenv()

#langchain graph 
from langchain.messages import HumanMessage
from langgraph.types import Command

from voice.tts import speak, wait_until_speech_done

import time
import argparse

from graph import graph
from voice.asr import listen, load_voice, load_scenario 


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--manual", action='store_true')
ap.add_argument("-t", "--test", action='store_true')
args = ap.parse_args()
#domyslnie test
test = args.test or not args.manual
manual = args.manual

print('args', args)

chat_config = {
    "configurable": {
        "thread_id": uuid.uuid4()
    }
}

if test:
    print("Test mode")
    scenario = load_scenario("test_scenarios/weather/")
    i = 0

    while i < len(scenario):
        sample = scenario[i]

        message = sample["text"]
        delay = sample["delay"]

        print(f"Pytanie [Tura {i}]: {message}")
        speak(message)

        result = graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=chat_config
        )

        if "__interrupt__" in result:
            question = result["__interrupt__"][0].value
            speak(question)
            wait_until_speech_done()

            # przejdź do następnej wiadomości scenariusza
            i += 1

            if i >= len(scenario):
                raise RuntimeError(
                    "Scenariusz zakończył się, ale agent oczekiwał odpowiedzi użytkownika."
                )

            answer = scenario[i]["text"]

            print(f"Odpowiedź użytkownika: {answer}")

            result = graph.invoke(
                Command(resume=answer),
                config=chat_config
            )

        response = result["messages"][-1].content
        print(response)
        wait_until_speech_done()

        i += 1

    print(scenario)
    

     

if manual: 
    listener = listen()
    for message, delay, reason in listener:

        if reason:
            print(f"asr fail: reason '{reason}'")
            speak("Nie zrozumiałem. Czy możesz powtórzyć?")
            continue

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

        
        print("Chat: " + result['messages'][-1].content)
        speak(response)
    
