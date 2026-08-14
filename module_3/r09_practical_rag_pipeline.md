# 9 – Practical RAG Pipeline

## Learning Objectives

After completing this lesson, I should be able to:

- Understand the two phases of RAG.
- Build the conceptual RAG ingestion pipeline.
- Load documents.
- Split documents into chunks.
- Create embeddings.
- Store embeddings in a vector store.
- Create a Retriever.
- Understand exactly how the user question reaches the Retriever.
- Understand how `RunnableParallel` passes the question to multiple branches.
- Combine retrieved context with the original question.
- Build a Prompt → Model → Parser pipeline.
- Understand the complete RAG flow in LangChain.
- Understand how to debug retrieval before blaming the LLM.

---

# 1. RAG Has Two Main Phases

RAG should be divided into two separate phases.

## Phase 1 — Ingestion

This prepares documents for future retrieval.

```text
Document
   ↓
Load
   ↓
Split
   ↓
Chunks
   ↓
Embedding Model
   ↓
Vectors
   ↓
Vector Store
```

## Phase 2 — Retrieval + Generation

This happens when the user asks a question.

```text
User Question
   ↓
Retrieve Relevant Chunks
   ↓
Question + Context
   ↓
Prompt
   ↓
LLM
   ↓
Answer
```

---

# 2. Phase 1 — Load Documents

LangChain provides document loaders.

Example:

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader("company_policy.txt")

documents = loader.load()
```

Conceptually:

```text
company_policy.txt
       ↓
TextLoader
       ↓
Document Objects
```

A LangChain `Document` generally contains:

```python
Document(
    page_content="...",
    metadata={...}
)
```

So a document contains:

```text
page_content
+
metadata
```

---

# 3. Phase 2 — Split Documents

Documents are usually too large to embed and retrieve as one giant piece.

We split them into chunks.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(documents)
```

Conceptually:

```text
Document
   ↓
Text Splitter
   ↓
Chunk 1
Chunk 2
Chunk 3
...
```

---

# 4. Important: `chunk_size` Is Not Necessarily Tokens

With:

```python
chunk_size=500
```

do not automatically interpret this as:

```text
500 tokens
```

`RecursiveCharacterTextSplitter` uses a character-based length function by default.

Different splitters and configurations can use different units.

Therefore:

```text
chunk_size
≠
automatically token count
```

---

# 5. Why Chunking?

Suppose:

```text
500-page PDF
```

If we create one vector:

```text
500-page PDF
      ↓
One Embedding
      ↓
One Vector
```

retrieval becomes less precise.

Instead:

```text
500-page PDF
      ↓
Chunks
      ↓
Embeddings
      ↓
Vectors
```

Now we can retrieve specific pieces of information.

---

# 6. Chunk Size Trade-Off

### Too Small

```text
Too little context
```

Important information may be split between chunks.

### Too Large

```text
Too much irrelevant information
```

This can increase:

* Token usage
* Prompt size
* Cost
* Retrieval noise

Therefore:

```text
Too Small ←──── Optimal ────→ Too Large
```

There is no universal perfect chunk size.

---

# 7. Chunk Overlap

Chunks can overlap.

Example:

```text
Chunk 1:
A B C D E F

Chunk 2:
E F G H I J
```

The overlap is:

```text
E F
```

Overlap helps preserve information near chunk boundaries.

---

# 8. Always Inspect Your Chunks

During development:

```python
for chunk in chunks:
    print(chunk.page_content)
    print(chunk.metadata)
    print("---")
```

Check:

* Are chunks meaningful?
* Are sentences being cut badly?
* Is there too much duplication?
* Is metadata preserved?
* Is the chunk size appropriate?

Do not blindly trust the chunking strategy.

---

# 9. Embeddings

Each chunk is converted into a numerical representation.

```text
Chunk
   ↓
Embedding Model
   ↓
Vector
```

Conceptually:

```text
"The annual leave request..."
        ↓
[0.12, -0.43, 0.81, ...]
```

The numbers are not human-readable meanings.

---

# 10. Query Embedding vs Document Embedding

During ingestion:

```text
Chunk
   ↓
Embedding Model
   ↓
Chunk Vector
```

During retrieval:

```text
Question
   ↓
Embedding Model
   ↓
Question Vector
```

Then:

```text
Question Vector
      ↓
Similarity Search
      ↓
Chunk Vectors
```

---

# 11. Store Vectors

For learning, an in-memory vector store can be used.

Conceptually:

```python
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(
    embedding_model
)

vector_store.add_documents(chunks)
```

The architecture becomes:

```text
Chunk 1 → Vector 1 ┐
Chunk 2 → Vector 2 ├──→ Vector Store
Chunk 3 → Vector 3 ┘
```

---

# 12. In-Memory vs Production

An in-memory store is useful for learning and experiments.

But:

```text
Application Restart
       ↓
Memory Lost
```

Production systems normally use a persistent vector store/database such as:

* PostgreSQL + pgvector
* Pinecone
* Qdrant
* Weaviate
* Milvus

depending on requirements.

---

# 13. Create a Retriever

A vector store can expose a Retriever.

Example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)
```

Now:

```text
Question
   ↓
Retriever
   ↓
Top 3 Relevant Documents
```

The Retriever hides some of the lower-level retrieval details.

---

# 14. The Most Important Question: How Does the Retriever Receive the Question?

There is no magic.

Your application explicitly passes the question to the Retriever.

Suppose:

```python
question = "How early should I request annual leave?"
```

Then:

```python
docs = retriever.invoke(question)
```

means:

```text
question
   ↓
retriever.invoke(question)
   ↓
Retriever
```

The Retriever receives the question because **your application passed it to the Retriever**.

---

# 15. What Happens Inside the Retriever?

Conceptually:

```text
Question
   ↓
Embedding Model
   ↓
Question Vector
   ↓
Vector Store
   ↓
Similarity Search
   ↓
Relevant Documents
```

So:

```python
docs = retriever.invoke(question)
```

can be mentally expanded to:

```text
"How early should I request annual leave?"
              ↓
        Question Embedding
              ↓
       Question Vector
              ↓
       Similarity Search
              ↓
        Relevant Chunks
```

The actual implementation may contain additional steps, but this is the correct mental model.

---

# 16. The Retriever Does Not Magically Know the User Question

This is very important.

Wrong mental model:

```text
User asks question
       ↓
Retriever somehow knows it
```

Correct:

```text
User
 ↓
Application
 ↓
question = "..."
 ↓
retriever.invoke(question)
 ↓
Retriever
```

The application/chain passes the input.

---

# 17. Direct Retriever Usage

Without LCEL:

```python
question = "How early should I request annual leave?"

docs = retriever.invoke(question)
```

Then:

```python
context = format_docs(docs)
```

Then:

```python
prompt_input = {
    "context": context,
    "question": question,
}
```

This is perfectly valid.

---

# 18. Why Do We Need RunnableParallel?

Now we can express the same data flow using LCEL.

```python
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
)
```

Example:

```python
rag_input = RunnableParallel(
    context=retriever,
    question=RunnablePassthrough(),
)
```

The important question is:

> What input does `RunnableParallel` receive?

It receives the user question when the chain is invoked.

For example:

```python
rag_input.invoke(
    "How early should I request annual leave?"
)
```

---

# 19. RunnableParallel Distributes the Question

Input:

```text
"How early should I request annual leave?"
```

enters:

```text
RunnableParallel
```

Then it sends the same input to both branches:

```text
                    Question
                       │
                       ▼
               RunnableParallel
                  /          \
                 /            \
                ↓              ↓
          Retriever       Passthrough
                ↓              ↓
        Relevant Chunks     Same Question
```

So conceptually:

```python
context = retriever.invoke(question)

original_question = question
```

are represented as two branches.

---

# 20. Why RunnablePassthrough?

The Retriever transforms the question:

```text
Question
   ↓
Retriever
   ↓
Relevant Chunks
```

But we also need the original question later.

So:

```text
Question
   ├──→ Retriever → Context
   │
   └──→ Passthrough → Question
```

`RunnablePassthrough` simply returns the input unchanged.

It does not store the value.

It is not Memory.

---

# 21. RunnablePassthrough Is Not Required

We could always use a Python variable:

```python
question = "How early should I request annual leave?"

docs = retriever.invoke(question)

data = {
    "context": format_docs(docs),
    "question": question,
}
```

This works perfectly.

The benefit of `RunnablePassthrough` is composition.

It lets the data flow be represented inside the Runnable graph.

---

# 22. The Result of RunnableParallel

Suppose:

```python
rag_input = RunnableParallel(
    context=retriever | RunnableLambda(format_docs),
    question=RunnablePassthrough(),
)
```

Then:

```python
rag_input.invoke(
    "How early should I request annual leave?"
)
```

produces conceptually:

```python
{
    "context": "...retrieved chunks...",
    "question": "How early should I request annual leave?"
}
```

Now both pieces are ready for the Prompt.

---

# 23. Format Retrieved Documents

The Retriever usually returns `Document` objects.

We can convert them into text:

```python
def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )
```

Flow:

```text
Documents
   ↓
format_docs()
   ↓
Text Context
```

---

# 24. Create the Prompt

Example:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using only the provided context.

    Context:
    {context}

    Question:
    {question}
    """
)
```

The prompt expects:

```text
context
+
question
```

---

# 25. Add the Model

Now:

```python
rag_input | prompt | model
```

Flow:

```text
Question
   ↓
RunnableParallel
   ↓
Context + Question
   ↓
Prompt
   ↓
Model
```

---

# 26. Add the Output Parser

Use:

```python
from langchain_core.output_parsers import StrOutputParser
```

Then:

```python
rag_chain = (
    rag_input
    | prompt
    | model
    | StrOutputParser()
)
```

Complete flow:

```text
Question
   ↓
Retriever + Passthrough
   ↓
Context + Question
   ↓
Prompt
   ↓
Model
   ↓
StrOutputParser
   ↓
Answer
```

---

# 27. Complete Conceptual Code

```python
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
embedding_model = ...


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


# 8. RAG input
rag_input = RunnableParallel(
    context=retriever | RunnableLambda(format_docs),
    question=RunnablePassthrough(),
)


# 9. Complete chain
rag_chain = (
    rag_input
    | prompt
    | model
    | StrOutputParser()
)


# 10. Ask question
answer = rag_chain.invoke(
    "How early should I request annual leave?"
)

print(answer)
```

---

# 28. Trace One Question Through the Chain

Suppose:

```text
Question:
"How early should I request annual leave?"
```

### Step 1

Application calls:

```python
rag_chain.invoke(question)
```

### Step 2

The question enters `RunnableParallel`.

```text
Question
   ↓
RunnableParallel
```

### Step 3

Retriever branch receives the question:

```text
Question
   ↓
Retriever
   ↓
Question Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
```

### Step 4

Passthrough branch receives the same question:

```text
Question
   ↓
Passthrough
   ↓
Same Question
```

### Step 5

The two branches produce:

```python
{
    "context": "...relevant chunks...",
    "question": "How early should I request annual leave?"
}
```

### Step 6

Prompt receives that dictionary.

### Step 7

Model receives the formatted prompt.

### Step 8

`StrOutputParser()` converts the model output into a string.

---

# 29. Retriever Does Not Answer the Question

The Retriever's job is:

```text
Question
   ↓
Relevant Documents
```

It doesn't normally produce the final answer.

The LLM produces the answer.

Therefore:

```text
Retriever
→ Finds evidence

LLM
→ Generates answer using evidence
```

---

# 30. VectorDB Does Not Answer the Question

Similarly:

```text
VectorDB
→ Stores/searches vectors
```

It doesn't reason about the question.

Think:

```text
Embedding Model
→ Converts text to numerical representation

VectorDB
→ Searches vector representations

Retriever
→ Returns relevant documents

LLM
→ Generates the answer
```

---

# 31. Why Do We Use a Retriever?

Instead of exposing every vector-search implementation detail to the rest of the application:

```text
Question
 ↓
Retriever
 ↓
Documents
```

The Retriever provides a higher-level abstraction.

Underneath, it might use:

```text
Vector Database
```

or another retrieval strategy such as:

```text
Keyword Search
Hybrid Search
```

The rest of the application can still work with:

```text
Retriever → Documents
```

---

# 32. Retrieval vs Generation

These are separate jobs.

## Retrieval

```text
Question
 ↓
Embedding
 ↓
Vector Search
 ↓
Relevant Chunks
```

Goal:

> Find information.

## Generation

```text
Question + Context
 ↓
LLM
 ↓
Answer
```

Goal:

> Generate an answer.

---

# 33. What If Retrieval Is Wrong?

Suppose the user asks:

```text
"What is the refund period?"
```

But retrieval returns:

```text
"Refunds require manager approval."
```

The LLM doesn't have the actual refund period.

Therefore:

```text
Bad Retrieval
     ↓
Bad Context
     ↓
Potentially Bad Answer
```

This is why retrieval quality must be checked before blaming the LLM.

---

# 34. Debugging RAG

Always inspect retrieved documents.

```python
docs = retriever.invoke(question)

for doc in docs:
    print(doc.page_content)
    print(doc.metadata)
    print("---")
```

Ask:

```text
Did I retrieve the correct information?
```

before asking:

```text
Why did the LLM give a bad answer?
```

---

# 35. Complete RAG Architecture

```text
                    INGESTION

Document
   ↓
Loader
   ↓
Chunks
   ↓
Embedding Model
   ↓
Vectors
   ↓
Vector Store


                    QUERY

User Question
      ↓
Application
      ↓
RAG Chain
      ↓
RunnableParallel
      │
      ├───────────────┐
      ↓               ↓
 Retriever       Passthrough
      ↓               ↓
Question Vector    Question
      ↓               │
Vector Search          │
      ↓               │
Relevant Chunks        │
      │               │
      └───────┬───────┘
              ↓
        Context + Question
              ↓
            Prompt
              ↓
             LLM
              ↓
        StrOutputParser
              ↓
           Answer
```

---

# 36. Don't Let These Become Blurred Again

```text
Chunk
  ↓
Piece of original text
```

```text
Token
  ↓
Unit produced by tokenizer
```

```text
Token ID
  ↓
Numeric identifier representing a token
```

```text
Embedding
  ↓
Semantic numerical representation
```

```text
Vector
  ↓
Numerical representation/array of the embedding
```

```text
VectorDB
  ↓
Stores / indexes / searches vectors
```

```text
Retriever
  ↓
Gets relevant documents/chunks
```

```text
Context
  ↓
Information supplied to the LLM
```

```text
LLM
  ↓
Generates the answer
```

### Compact form

```text
Chunk
≠ Token
≠ Token ID
≠ Embedding
≠ VectorDB
≠ Retriever
≠ Context
≠ LLM
```

---

# 37. Most Important Mental Model From This Lesson

The question doesn't magically reach the Retriever.

It follows a data flow:

```text
User
 ↓
Your Application
 ↓
question = "..."
 ↓
rag_chain.invoke(question)
 ↓
RunnableParallel
 ├──→ Retriever(question)
 │       ↓
 │   Relevant Chunks
 │
 └──→ Passthrough(question)
         ↓
      Original Question
```

Then:

```text
Relevant Chunks + Original Question
              ↓
            Prompt
              ↓
             LLM
              ↓
           Answer
```

---

# 38. One-Line Summary

> **A practical RAG pipeline loads and chunks documents, embeds and stores them in a vector store, then passes the user's question into a Retriever to find relevant chunks; those chunks and the original question are combined into a prompt and sent to the LLM to generate the final answer.**

---

## Connections

Previous:

* **R08 – RAG Fundamentals**

Current:

* **R09 – Practical RAG Pipeline**

Next:

* **R10 – Retrieval Quality & Advanced Retrieval**

---

# Final Mental Model

```text
User Question
      ↓
Your Application
      ↓
rag_chain.invoke(question)
      ↓
RunnableParallel
      │
      ├───────────────┐
      ↓               ↓
 Retriever       Passthrough
      ↓               ↓
Relevant Chunks   Original Question
      │               │
      └───────┬───────┘
              ↓
        Context + Question
              ↓
            Prompt
              ↓
             LLM
              ↓
           Answer
```

The Retriever receives the question because the chain's input is the question, and `RunnableParallel` passes that input to the Retriever branch.
