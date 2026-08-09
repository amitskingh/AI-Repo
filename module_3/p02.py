from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")


messages = [
    HumanMessage(content="What is Python?"),
    AIMessage(content="Python is a programming language."),
    HumanMessage(content="What was my previous question about?"),
]

response = model.invoke(messages)

print(response.content)
