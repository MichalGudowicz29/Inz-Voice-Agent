import time

from agents.assistant import llm
from langchain.messages import AIMessage, SystemMessage
from prompts import assistant_prompt, planner_prompt
from voice.tts import speak
from agents.planner import planner_agent
from agents.assistant import assistant_agent
from .state import State



# node
# glowny asystent wejsciowy
def assistant_node(state: State):

    ct0 = time.time()
    
    response = assistant_agent([*state["messages"]])

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

    response = planner_agent([*state["messages"]])

    print(f"Planner ({time.time() - pt0:.3f}s)")
    print(response)

    return {
        "plan": response.steps,
        "action": "verify_plan" 
    }




