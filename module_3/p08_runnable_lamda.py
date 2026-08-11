from langchain_core.runnables import RunnableLambda

def uppercase(text: str) -> str:
    return text.upper()


uppercase_runnable = RunnableLambda(uppercase)
result: str = uppercase_runnable.invoke("hello world")  # Returns "HELLO WORLD"

print(result)  # Output: HELLO WORLD
