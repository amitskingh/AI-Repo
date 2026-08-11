from langchain_core.runnables import RunnableLambda


def double(x):
    return x * 2


def square(x):
    return x * x


double_runnable = RunnableLambda(double)
square_runnable = RunnableLambda(square)

chain = double_runnable | square_runnable


result = chain.invoke(3)  # Returns 36
print(result)  # Output: 36
