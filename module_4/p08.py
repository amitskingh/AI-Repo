from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command


class GraphState(TypedDict):
    task: str
    approval: str
    result: str


def prepare(state: GraphState):
    return {"result": f"Prepared: {state['task']}"}


def request_approval(state: GraphState):
    # Pause here and ask the caller for approval.
    approval = interrupt({
        "question": "Approve this action?",
        "prepared_result": state["result"],
    })
    return {"approval": approval}


def finish(state: GraphState):
    if state["approval"] == "yes":
        return {"result": state["result"] + " — approved"}
    return {"result": "Action cancelled"}


builder = StateGraph(GraphState)
builder.add_node("prepare", prepare)
builder.add_node("request_approval", request_approval)
builder.add_node("finish", finish)

builder.add_edge(START, "prepare")
builder.add_edge("prepare", "request_approval")
builder.add_edge("request_approval", "finish")
builder.add_edge("finish", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "approval-demo-1"}}

# First call: runs until interrupt() pauses the graph.
paused = graph.invoke(
    {"task": "Send the community notice", "approval": "", "result": ""},
    config,
)
print("Paused:", paused)

# Second call: resume the same paused run with the approval response.
resumed = graph.invoke(Command(resume="yes"), config)
print("Resumed:", resumed)