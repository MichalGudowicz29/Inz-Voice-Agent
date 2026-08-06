from typing import Annotated, Literal, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    action: Literal[
        "chat",
        "planner",
        "ask_user",
        "verify_plan",
    ]
    task: str
    plan: list[str]
    verification: dict
    clarification_question: str
    execution_results: list
    executor_success: bool
    executor_fail_reasoning: str
    final_answer: str
