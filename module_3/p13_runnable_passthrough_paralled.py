from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)


def create_context(question: str) -> str:
    return f"Relevant information for: {question}"


context = RunnableLambda(create_context)


chain = RunnableParallel(
    context=context,
    question=RunnablePassthrough(),
)


result: str = chain.invoke("What is RAG?")

# Output: {'context': 'Relevant information for: What is RAG?', 'question': 'What is RAG?'}
print(result)
