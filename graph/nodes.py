import time

from agents.assistant import llm
from langchain.messages import AIMessage, SystemMessage
from prompts import assistant_prompt
from voice.tts import speak
from .state import State



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
