from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph

from .nodes import assistant_node, planner_node, verification_node
from .state import State


checkpointer = InMemorySaver(
    serde=JsonPlusSerializer(
        allowed_msgpack_modules=[
            ("agents.assistant", "AgentOutput"),
            ("agents.planner", "PlanOutput")
        ]
    )
)
# defining nodes
builder = StateGraph(State)
builder.add_node("assistant_node", assistant_node)
builder.add_node("planner", planner_node)
builder.add_node("verification", verification_node)


# building graph
builder.add_edge(START, "assistant_node")
builder.add_conditional_edges(
    "assistant_node",
    lambda state: state["action"],
    #path map do grafiki
    {
        "chat": END,
        "planner": "planner"
    }
)
builder.add_conditional_edges(
    "planner",
    lambda state: END if state["action"] == "ask_user" else "verification",  
    #path map do grafiki
    {
        "verification":"verification",
        END: END
            
    }
)
builder.add_edge("verification", END)


graph = builder.compile(checkpointer=checkpointer)


def write_graph_png(path: str = "agent_graph.png") -> None:
    try:
        png = graph.get_graph().draw_mermaid_png()
    except Exception as exc:
        print(f"Graph image generation skipped: {type(exc).__name__}")
        return

    with open(path, "wb") as f:
        f.write(png)


write_graph_png()
