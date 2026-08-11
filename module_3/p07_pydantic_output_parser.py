from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


load_dotenv()


# -------------------------
# 1. Pydantic Output Parser
# -------------------------

parser = PydanticOutputParser(pydantic_object=Person)


# -------------------------
# 2. Prompt
# -------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an information extraction assistant.

            You MUST return exactly one JSON object.

            The JSON object must have exactly these fields:
            - name: a single string
            - age: a single integer

            Do NOT use arrays.
            Do NOT put values inside [].
            """,
        ),
        (
            "human",
            """
            Here is a short story:

            Rahul is a 25-year-old software engineer who loves
            building AI applications.

            Extract the person's name and age.

            {format_instructions}
            """,
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())


# -------------------------
# 3. Hugging Face model
# -------------------------

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    max_new_tokens=100,
)

model = ChatHuggingFace(llm=llm)


# -------------------------
# 4. Chain
# -------------------------

chain = prompt | model | parser


# -------------------------
# 5. Invoke
# -------------------------

result = chain.invoke({})


print(result)
print("Name:", result.name)
print("Age:", result.age)
