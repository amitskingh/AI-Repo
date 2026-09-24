from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel


class GraphState(BaseModel):
    message: str


def greet(state: GraphState) -> GraphState:

    print("Node received state: ", state)

    return GraphState(message=state.message + " 👋")

graph_builder = StateGraph(GraphState)
graph_builder.add_node("greet", greet)
graph_builder.add_edge(START, "greet")
graph_builder.add_edge("greet", END)

graph = graph_builder.compile()


if __name__ == "__main__":
    result = graph.invoke({"message": "Hello, LangGraph!"})

    print("Final result: ", result)
