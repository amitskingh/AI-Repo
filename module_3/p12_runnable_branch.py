from langchain_core.runnables import RunnableBranch, RunnableLambda


def is_positive(x: int) -> bool:
    return x > 0


def positive(x: int) -> str:
    return "Positive"


def negative(x: int) -> str:
    return "Negative"


branch = RunnableBranch(
    (lambda x: is_positive(x), RunnableLambda(positive)), RunnableLambda(negative)
)


result: str = branch.invoke(5)
print(result)  # Output: "Positive"

result: str = branch.invoke(-3)
print(result)  # Output: "Negative"