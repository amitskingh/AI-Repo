from langchain_core.runnables import RunnableParallel, RunnableLambda

def double(x):
    return x * 2


def square(x):
    return x * x

double_runnable = RunnableLambda(double)
square_runnable = RunnableLambda(square)

parallel = RunnableParallel(
    double=double_runnable,
    square=square_runnable,
)


result = parallel.invoke(3)  # Returns {'double': 6, 'square': 9}
print(result)  # Output: {'double': 6, 'square': 9}
