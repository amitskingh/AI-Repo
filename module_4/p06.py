from typing import Annotated, TypedDict
from operator import add

from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
    answer: str
    messages: Annotated[list[str], add]

def first_node(state: GraphState):
    return {
        "answer": "First answer",
        "messages": ["First message"],
    }

def second_node(state: GraphState):
    return {
        "answer": "Updated answer",
        "messages": ["Second message"],
    }

builder = StateGraph(GraphState)
builder.add_node("first", first_node)
builder.add_node("second", second_node)

builder.add_edge(START, "first")
builder.add_edge("first", "second")
builder.add_edge("second", END)

graph = builder.compile()

result = graph.invoke({
    "answer": "Initial answer",
    "messages": ["Initial message"],
})

print(result)