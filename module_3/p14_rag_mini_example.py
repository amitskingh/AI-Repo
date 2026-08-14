from typing import Any, Dict
from langchain_core.retrievers import RetrieverInput
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


# 0. Model
model = ChatOpenAI(model="gpt-4o-mini")

# 1. Load
loader = TextLoader("company_policy.txt")
documents = loader.load()


# 2. Split
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)


# 3. Embedding model
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


# 4. Vector store
vector_store = InMemoryVectorStore(
    embedding_model
)

vector_store.add_documents(chunks)


# 5. Retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# 6. Prompt
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using only the provided context.

    Context:
    {context}

    Question:
    {question}
    """
)


# 7. Format documents
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# 8. RAG chain
rag_chain = (
    RunnableParallel[RetrieverInput, Dict[str, str]](
        context=retriever | RunnableLambda[Any, str](format_docs),
        question=RunnablePassthrough[RetrieverInput](),
    )
    | prompt
    | model
    | StrOutputParser()
)


# 9. Ask
answer = rag_chain.invoke(
    "How early should I request annual leave?"
)

print(answer)