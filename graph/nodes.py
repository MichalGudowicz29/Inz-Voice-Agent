import time

from agents.assistant import llm
from langchain.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.types import interrupt
from prompts import assistant_prompt, planner_prompt
from voice.tts import speak
from agents.planner import planner_agent
from agents.assistant import assistant_agent
from agents.verifier import verification_agent
from agents.executor import executor_agent
from agents.synthesizer import synthesizer_agent
from .state import State



# node
# glowny asystent wejsciowy
def assistant_node(state: State):

    ct0 = time.time()
    
    response = assistant_agent([*state["messages"]])

    print(f"Conversation node: {time.time() - ct0:.3f}s")
    print(f"Action {response.action}")
    
    if response.answer:
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
    success = state.get("executor_success", True)
    reason = state.get("executor_fail_reasoning", "")

    response = planner_agent([*state["messages"]], success, reason)

    print(f"Planner ({time.time() - pt0:.3f}s)")

    if response.needs_clarification:
        clarification = interrupt(response.clarification_question)
        state["messages"].append(HumanMessage(content=clarification))
        response = planner_agent([*state["messages"]], success, reason)

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
    response = executor_agent(state["task"], state["plan"])
    print(f"Execution: {time.time() - et0}")

    output = response["structured_response"]

    print(output.final_answer)

    if output.success:
        return {
        "messages": [AIMessage(content=output.final_answer)],
        "execution_results": output,
        "final_answer": output.final_answer,
        "executor_success": output.success,
    }


    return {
            "execution_results": output,
            "final_answer": output.final_answer,
            "executor_fail_reasoning": output.failure_reason,
            "executor_success": output.success,
        }


#synthesizer

def synthesizer_node(state: State):
    st0 = time.time()
    response = synthesizer_agent(state["task"], state["final_answer"])
    print(f"Synthesizer: {time.time() - st0}")

    output = response["structured_response"]

    speak(output.spoken_response)


    return {
        "messages": [AIMessage(content=output.spoken_response)] 
        }



    



