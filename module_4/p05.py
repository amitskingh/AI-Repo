from typing import Literal

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


# In a real app, derive this from trusted authentication/session context.
# Do not accept it from the user's message or let the LLM choose it.
authorized_community_ids = {101}

@tool
def get_maximum_fine(community_id: int, year: int) -> str:
    """Look up the maximum fine for a community and policy year."""
    if community_id not in authorized_community_ids:
        return "Access denied: you are not authorized to access this community."

    fines = {
        (101, 2025): 500,
        (101, 2026): 1000,
        (102, 2026): 5000,
    }

    amount = fines.get((community_id, year))
    if amount is None:
        return "No policy data found."

    return f"Maximum fine: ${amount}"


tools = [get_maximum_fine]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)


def call_llm(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("llm", call_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "llm")

builder.add_conditional_edges(
    "llm",
    tools_condition,
)

builder.add_edge("tools", "llm")

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What is the maximum fine for Community 102 in 2026?"
                )
            ]
        }
    )

    print(result["messages"][-1].content)
