from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict):
    count: int


def increment(state: GraphState):
    return {"count": state["count"] + 1}


builder = StateGraph(GraphState)
builder.add_node("increment", increment)
builder.add_edge(START, "increment")
builder.add_edge("increment", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "conversation-1"}}

first_result = graph.invoke({"count": 0}, config)
print(first_result)  # {"count": 1}

second_result = graph.invoke({"count": 1}, config)

print(second_result)  # resumes from saved state; count becomes 2