from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class GraphState(TypedDict):
    attempts: int
    max_attempts: int
    score: int
    result: str


def generate_answer(state: GraphState):
    attempt = state["attempts"] + 1

    # Simulate an answer improving with each attempt.
    score = {1: 40, 2: 55}.get(attempt, 85)

    print(f"Generating answer: attempt {attempt}, score {score}")

    return {
        "attempts": attempt,
        "score": score,
    }


def evaluate_answer(state: GraphState):
    if state["score"] >= 70:
        result = "good"
    else:
        result = "poor"

    print("Evaluation:", result)
    return {"result": result}


def route_after_evaluation(
    state: GraphState,
) -> Literal["success", "retry", "give_up"]:

    if state["result"] == "good":
        return "success"

    if state["attempts"] >= state["max_attempts"]:
        return "give_up"

    return "retry"


def success_node(state: GraphState):
    print("Answer accepted!")
    return {}


def give_up_node(state: GraphState):
    print("Maximum attempts reached. Stopping.")
    return {}


builder = StateGraph(GraphState)

builder.add_node("generate", generate_answer)
builder.add_node("evaluate", evaluate_answer)
builder.add_node("success", success_node)
builder.add_node("give_up", give_up_node)

builder.add_edge(START, "generate")
builder.add_edge("generate", "evaluate")

builder.add_conditional_edges(
    "evaluate",
    route_after_evaluation,
    {
        "success": "success",
        "retry": "generate",
        "give_up": "give_up",
    },
)

builder.add_edge("success", END)
builder.add_edge("give_up", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "attempts": 0,
            "max_attempts": 3,
            "score": 0,
            "result": "",
        }
    )

    print("Final state:", result)
