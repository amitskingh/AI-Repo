from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")

# Create a prompt template using a list of messages
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful teacher."),
        ("human", "Explain {topic} in simple terms."),
    ]
)

# Create a chain by combining the prompt and the model
chain = prompt | model

response = chain.invoke({"topic": "embeddings"})

print(response.content)
