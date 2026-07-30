import time

from agents.assistant import llm
from langchain.messages import AIMessage, SystemMessage
from prompts import assistant_prompt, planner_prompt
from voice.tts import speak
from agents.planner import planner_agent
from agents.assistant import assistant_agent
from agents.verifier import verification_agent
from .state import State



# node
# glowny asystent wejsciowy
def assistant_node(state: State):

    ct0 = time.time()
    
    response = assistant_agent([*state["messages"]])

    print(f"Conversation node: {time.time() - ct0:.3f}s")
    print(f"Action {response.action}")

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
    print(f"Starting planning...")
    response = planner_agent([*state["messages"]])
    print(f"Planner ({time.time() - pt0:.3f}s)")

    if response.needs_clarification:
        speak(response.clarification_question)
        return {
            "messages": [AIMessage(content=response.clarification_question)],
            "plan": [],
            "action": "ask_user",
            "task": response.task
        }


    return {
        "plan": response.steps,
        "action": "verify_plan",
        "task": response.task 
    }


# weryfikator 
def verification_node(state: State):
    vt0 = time.time()
    
    response = verification_agent(state["task"], state["plan"])

    print(f"Verification: {time.time() - vt0}")

    return {"verification": 
              {
                "verified": response.verified, 
                "reasoning": response.reasoning
              }
           }

# exec
def execution_node(state: State):
    et0 = time.time() 
    print(" I am executing something... ")
    return {"execution_results": ['abc','abc']}




