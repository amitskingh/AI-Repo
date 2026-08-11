from langchain_core.runnables import RunnablePassthrough

passthrough_runnable = RunnablePassthrough()
result: str = passthrough_runnable.invoke("hello world")  # Returns "hello world"
print(result)  # Output: hello world