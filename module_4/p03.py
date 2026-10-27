from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict):
    score: int
    result: str


def evaluate(state: GraphState):
    print("Evaluating score:", state["score"])

    if state["score"] >= 70:
        return {"result": "Good answer"}
    else:
        return {"result": "Poor answer"}


def route_after_evaluation(
    state: GraphState,
) -> Literal["success", "retry"]:
    if state["result"] == "Good answer":
        return "success"

    return "retry"


def success_node(state: GraphState):
    print("Answer accepted")
    return {}


def retry_node(state: GraphState):
    print("Answer needs improvement")
    return {}


builder = StateGraph(GraphState)

builder.add_node("evaluate", evaluate)
builder.add_node("success_node", success_node)
builder.add_node("retry_node", retry_node)

builder.add_edge(START, "evaluate")

builder.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "success": "success_node",
        "retry": "retry_node",
    },
)

builder.add_edge("success_node", END)
builder.add_edge("retry_node", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "score": 85,
            "result": "",
        }
    )

    print("Final state:", result)
