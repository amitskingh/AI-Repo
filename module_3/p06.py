from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


load_dotenv()

prompts = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant."
    ),
    (
        "human",
        """Alice is a 30-year-old software developer.
Extract her name and age."""
    ),
])

model = ChatOpenAI(model="gpt-4o-mini")

structured_model = model.with_structured_output(Person)

chain = prompts | structured_model

result = chain.invoke({})

print(result)