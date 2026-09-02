from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from src.rag.llm import llm
from src.rag.prompt import RAG_PROMPT
from src.retrieval.vector_store import create_vector_store


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)



# Create the vector store
vector_store = create_vector_store()

def create_retriever(community_id, version):
    return vector_store.as_retriever(
        search_kwargs={
            "k": 3,
            "filter": {
                "$and": [
                    {"community_id": community_id},
                    {"version": version},
                ]
            },
        }
    )


# Create the retriever from the vector store
retriever = create_retriever(community_id=102, version=2026)


# Build the RAG chain
rag_chain = (
    RunnableParallel(
        context=retriever | format_docs,
        question=RunnablePassthrough(),
    )
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)


if __name__ == "__main__":
    question = "How much can I be fined?"

    answer = rag_chain.invoke(question)

    print("=" * 60)
    print("Question:")
    print(question)

    print("=" * 60)
    print("Answer:")
    print(answer)