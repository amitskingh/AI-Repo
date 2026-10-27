from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


class GraphState(BaseModel):
    message: str


def greet(state: GraphState) -> GraphState:

    print("Node received state: ", state)

    return GraphState(message=state.message + " 👋")

graph = StateGraph(GraphState)
graph.add_node("greet", greet)
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

graph = graph.compile()


if __name__ == "__main__":
    result = graph.invoke({"message": "Hello, LangGraph!"})

    print("Final result: ", result)
