from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


model = ChatOpenAI(model="gpt-4o-mini")

prompt = PromptTemplate.from_template("Explain {topic} to a {audience} using {style}.")


result = prompt.invoke(
    {
        "topic": "RAG",
        "audience": "beginner",
        "style": "a simple example",
    }
)

print(result)

response = model.invoke(result)

print(response.content)
