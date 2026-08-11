from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompts = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "Explain {topic} in single sentence."),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini")

parser = StrOutputParser()

chain = prompts | model | parser

result = chain.invoke({"topic": "embeddings"})

print(result)
