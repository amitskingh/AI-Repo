from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel


class GraphState(BaseModel):
    message: str


def add_greeting(state: GraphState) -> GraphState:
    print("Node received state: ", state)
    return GraphState(message=state.message + " 👋")


def add_signature(state: GraphState) -> GraphState:
    print("Node received state: ", state)
    return GraphState(message=state.message + " - LangGraph")


if __name__ == "__main__":
    graph = StateGraph(GraphState)
    graph.add_node("add_greeting", add_greeting)
    graph.add_node("add_signature", add_signature)
    graph.add_edge(START, "add_greeting")
    graph.add_edge("add_greeting", "add_signature")
    graph.add_edge("add_signature", END)

    graph = graph.compile()

    result = graph.invoke({"message": "Hello, LangGraph!"})

    print("Final result: ", result)
