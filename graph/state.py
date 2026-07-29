from typing import Annotated, Literal, TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    action: Literal[
        "chat",
        "planner",
        "weather",
        "search",
        "calendar",
        "ask_user"
    ]
