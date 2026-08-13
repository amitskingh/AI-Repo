# 8 – RAG Fundamentals: Chunks, Embeddings, VectorDB & Retrieval

## Learning Objectives

After completing this lesson, I should be able to:

- Explain what RAG is.
- Explain why documents are split into chunks.
- Understand the difference between chunks, tokens, embeddings, and vectors.
- Understand the ingestion/indexing phase of RAG.
- Understand the query/retrieval phase of RAG.
- Understand how a question becomes a query vector.
- Understand similarity search.
- Understand what a Vector Database does.
- Understand what a Retriever does.
- Understand why retrieved text is sent to the LLM instead of vectors.
- Understand Top-K retrieval.
- Understand metadata.
- Understand chunk overlap.
- Understand why RAG is not fine-tuning.
- Understand why large user questions may require query transformation.
- Connect RAG with Runnables and LCEL.

---

# 1. What Is RAG?

RAG stands for:

> **Retrieval-Augmented Generation**

The basic idea is:

> Retrieve relevant information first, then provide that information to the LLM so it can generate an answer.

Instead of sending every document to the LLM:

```text
All Documents
     ↓
LLM
```

we do:

```text
Question
   ↓
Retrieve Relevant Information
   ↓
Relevant Context
   ↓
LLM
   ↓
Answer
```

---

# 2. Why Do We Need RAG?

Suppose an application has:

```text
1,000 PDFs
10,000 pages
Millions of words
```

We don't want to send all of them to the LLM for every question.

Problems include:

* Context-window limitations
* Higher token consumption
* Higher cost
* More processing
* Irrelevant information
* Potentially worse answers

Instead:

```text
Millions of words
      ↓
Retrieve only relevant information
      ↓
Small amount of useful context
      ↓
LLM
```

---

# 3. High-Level RAG Flow

## Ingestion

```text
Documents
    ↓
Chunking
    ↓
Chunks
    ↓
Embedding Model
    ↓
Vectors
    ↓
Vector Database
```

## Query

```text
User Question
    ↓
Embedding Model
    ↓
Question Vector
    ↓
Similarity Search
    ↓
Relevant Chunks
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

# 4. Chunk

A chunk is a smaller piece of the original document.

Example:

```text
Original Document
        ↓
Large Text
        ↓
Smaller Meaningful Pieces
        ↓
Chunks
```

Example:

```text
Chunk 1:
"The association shall conduct an annual meeting
of its members during the month of March."

Chunk 2:
"Notice shall be provided to all members..."
```

A chunk remains human-readable text.

---

# 5. Why Do We Chunk?

Suppose a document has 500 pages.

If we create one embedding for the entire document:

```text
500-page Document
       ↓
One Embedding
       ↓
One Vector
```

Retrieval becomes less precise.

Instead:

```text
500-page Document
       ↓
Chunks
       ↓
Many Embeddings
       ↓
Many Vectors
```

Now the system can retrieve only the relevant portions.

---

# 6. Chunking Is Not Similarity Search

Important distinction:

```text
Chunking
→ "How should I divide this document?"

Similarity Search
→ "Which chunks are relevant to this question?"
```

Similarity is generally determined later during retrieval.

Chunking may consider:

* Paragraphs
* Sentences
* Headings
* Sections
* Character limits
* Token limits
* Document structure

The goal is to create chunks that preserve enough meaning while remaining small enough for efficient retrieval.

---

# 7. Chunk Size

If chunks are too small:

```text
Too little context
```

Example:

```text
"The association shall..."
```

The important information may be in the next chunk.

If chunks are too large:

```text
Too much irrelevant information
```

This can increase:

* Prompt size
* Token usage
* Cost
* Retrieval noise

Therefore:

```text
Too Small ←──── Optimal ────→ Too Large
```

There is no universal perfect chunk size.

Chunk size should be evaluated based on the specific data and application.

---

# 8. Chunk Overlap

Chunks can sometimes overlap.

Example:

```text
Chunk 1:
A B C D E F

Chunk 2:
E F G H I J
```

The overlapping portion is:

```text
E F
```

Overlap can help preserve context around chunk boundaries.

---

# 9. Chunk Metadata

A chunk can have metadata associated with it.

Example:

```python
{
    "text": "The association shall conduct an annual meeting...",
    "metadata": {
        "document": "Bylaws.pdf",
        "page": 15,
        "section": "Annual Meetings"
    }
}
```

Metadata can include:

```text
document_id
document_name
page_number
section
community_id
document_type
year
```

Metadata becomes useful for:

* Filtering
* Source identification
* Debugging
* Citations
* Security/access control
* Better retrieval

---

# 10. Token

A token is a unit produced by a tokenizer.

A token is not necessarily the same as a word.

For example, depending on the tokenizer:

```text
word
```

could be one token, while another word could be represented by multiple tokens.

Tokens can also represent pieces of words, punctuation, whitespace, etc., depending on the tokenizer.

---

# 11. Token ID

A tokenizer can map tokens to numerical IDs.

Conceptually:

```text
Text
 ↓
Tokenizer
 ↓
Tokens
 ↓
Token IDs
```

Important:

```text
Token
≠
Token ID
```

And:

```text
Token
≠
Embedding
```

A token is not simply a "word ID."

---

# 12. Embedding

An embedding is a numerical representation of text produced by an embedding model.

Example:

```text
"The dog is sleeping."
```

might produce something conceptually like:

```text
[
    0.12,
   -0.43,
    0.87,
    0.21,
    ...
]
```

The vector is a numerical representation of semantic information.

The individual numbers are not intended to be human-readable meanings.

---

# 13. Vector

The numerical representation produced by an embedding model is commonly represented as a vector.

Example:

```text
[0.12, -0.43, 0.87, 0.21, ...]
```

So:

```text
Text
 ↓
Embedding Model
 ↓
Embedding Vector
```

Do not think of every number as representing a specific word or concept that humans can directly interpret.

---

# 14. The Important Relationship

The ingestion process can be visualized as:

```text
Chunk
 ↓
Tokenizer
 ↓
Tokens / Token IDs
 ↓
Embedding Model
 ↓
Embedding Vector
```

Therefore:

```text
Chunk
≠
Token
≠
Embedding
≠
Vector Database
```

---

# 15. Embedding a Chunk

Suppose we have:

```text
Chunk:
"The association shall conduct an annual meeting..."
```

The embedding process is conceptually:

```text
Chunk
 ↓
Tokenizer
 ↓
Tokens / Token IDs
 ↓
Embedding Model
 ↓
Vector
```

That vector is then stored/indexed for retrieval.

---

# 16. Why Embeddings?

Suppose we have:

```text
A:
"The dog is sleeping."

B:
"The puppy is resting."

C:
"The database uses PostgreSQL."
```

The embedding model attempts to represent their semantic characteristics in vector space.

Conceptually:

```text
A ───── B


        C
```

A and B may be closer because they discuss similar concepts.

C may be farther away.

---

# 17. Vector Database

A Vector Database is designed to store and search vector representations efficiently.

Examples include:

* Pinecone
* pgvector/PostgreSQL
* Qdrant
* Weaviate
* Milvus

A vector store commonly associates a vector with information such as:

```text
Vector
+
Text / Document
+
Metadata
+
ID
```

or with a reference/ID that can be used to retrieve the original text elsewhere.

---

# 18. Important Question: Does VectorDB Store Only Vectors?

Not necessarily.

A vector store may look conceptually like:

```text
Vector Record
─────────────────────────────
ID: chunk_123

Vector:
[0.12, -0.34, ...]

Text:
"Annual meeting shall..."

Metadata:
{
    page: 15,
    document: "Bylaws.pdf"
}
```

Another architecture may separate the vector index from the canonical text storage:

```text
VectorDB
 ├── Vector
 └── Document ID

PostgreSQL
 └── Document Text
```

Then:

```text
Vector Search
     ↓
Document ID
     ↓
PostgreSQL
     ↓
Actual Text
```

Both architectures can be valid depending on application requirements.

---

# 19. Ingestion Pipeline

The ingestion phase prepares documents for retrieval.

```text
Document
   ↓
Load
   ↓
Chunk
   ↓
Tokenize
   ↓
Embed
   ↓
Store / Index Vector
```

More accurately:

```text
Document
   ↓
Chunks
   ↓
Embedding Model
   ↓
Vectors
   ↓
VectorDB
```

Tokenization happens internally when the model processes the text.

---

# 20. Query-Time Retrieval

Suppose the user asks:

```text
"What is the annual meeting requirement?"
```

We don't compare the raw question directly against raw document text in a typical vector-search RAG pipeline.

Instead:

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
Vector Search
       ↓
Similar Chunk Vectors
       ↓
Relevant Chunks
```

---

# 21. Question Embedding

At query time:

```text
User Question
     ↓
Embedding Model
     ↓
Question Vector
```

The question is generally embedded directly.

We do not normally chunk a short question like we chunk documents.

---

# 22. What If the Question Is Very Large?

A large user input may require additional processing.

For example:

```text
Large User Input
       ↓
Query Analysis
       ↓
Extract / Rewrite Query
       ↓
Embedding
       ↓
Retrieval
```

Possible techniques include:

* Query rewriting
* Query extraction
* Query decomposition
* Summarization
* Multiple retrieval queries

Example:

```text
Large User Request
       ↓
Query Rewriting
       ↓
"What are the annual meeting requirements?"
       ↓
Embedding
       ↓
Vector Search
```

The important point is:

> Document chunking and query transformation are different problems.

---

# 23. What If the Question Contains Instructions?

A user message can contain both instructions and an information need.

Example:

```text
"You are an HOA expert. Analyze the bylaws
and tell me whether the annual meeting requirement
is satisfied."
```

The entire message does not necessarily have to become the retrieval query.

We may derive:

```text
Retrieval Query:
"What are the annual meeting requirements?"
```

while the final prompt contains:

```text
Instructions
+
Retrieved Context
+
Question
```

This is an advanced RAG technique.

---

# 24. Multiple Questions

Suppose the user asks:

```text
When is the annual meeting held,
who must receive notice,
and what happens if notice is not provided?
```

This may represent multiple retrieval needs:

```text
Question
   ↓
Decomposition
   ├── Annual meeting timing
   ├── Notice requirements
   └── Failure to provide notice
```

Each query can potentially retrieve different chunks.

This is called:

> Query Decomposition

---

# 25. Similarity Search

Suppose we have:

```text
Question Vector
```

and stored vectors:

```text
Chunk A → Vector A
Chunk B → Vector B
Chunk C → Vector C
Chunk D → Vector D
```

The vector search compares the query vector with stored vectors.

Common similarity/distance approaches include:

* Cosine similarity
* Dot product
* Euclidean distance

Conceptually:

```text
Question Vector
      ↓
Compare against Chunk Vectors
      ↓
Rank by similarity/distance
      ↓
Top-K Results
```

---

# 26. What Exactly Is Being Compared?

Not:

```text
Question Text
     vs
Chunk Text
```

in a vector-search system.

Instead:

```text
Question Vector
     vs
Chunk Vectors
```

For example:

```text
Question Vector
       ↓
0.91 → Chunk A
0.87 → Chunk B
0.22 → Chunk C
0.12 → Chunk D
```

The exact score meaning depends on the similarity metric and implementation.

---

# 27. Top-K Retrieval

Suppose we have:

```text
10,000 chunks
```

We don't send all 10,000 to the LLM.

We might retrieve:

```text
Top 5
```

or:

```text
Top 10
```

Conceptually:

```text
10,000 Chunks
      ↓
Similarity Search
      ↓
Top-K
      ↓
5 Relevant Chunks
```

---

# 28. What Does the Retriever Return?

A Retriever generally returns relevant documents/chunks.

Conceptually:

```python
[
    {
        "text": "The annual meeting shall...",
        "metadata": {
            "page": 42,
            "document": "Bylaws.pdf"
        }
    },
    {
        "text": "Notice must be provided...",
        "metadata": {
            "page": 43,
            "document": "Bylaws.pdf"
        }
    }
]
```

The exact structure depends on the implementation.

---

# 29. Retriever

A Retriever is a higher-level interface for retrieving relevant information.

Conceptually:

```text
Question
   ↓
Retriever
   ↓
Relevant Documents / Chunks
```

A Retriever may internally use:

```text
Embedding Model
+
Vector Database
+
Similarity Search
```

So:

```text
Retriever
   ↓
High-level retrieval interface
```

while:

```text
VectorDB
   ↓
Vector storage/search infrastructure
```

---

# 30. Retriever vs VectorDB

Do not confuse them.

### Vector Database

```text
Stores/indexes/searches vectors
```

### Retriever

```text
Given a query, returns relevant documents/chunks
```

Conceptually:

```text
Question
   ↓
Retriever
   ↓
Vector Search
   ↓
Relevant Chunks
```

The Retriever may use a VectorDB internally.

---

# 31. Why Does the LLM Receive Text Instead of Vectors?

Suppose similarity search gives:

```text
Chunk A → 0.91
Chunk B → 0.87
```

The LLM normally doesn't need:

```text
0.91
0.87
```

It needs the retrieved information:

```text
Chunk A:
"Annual meetings shall be held..."

Chunk B:
"Notice shall be provided..."
```

Therefore:

```text
VectorDB
   ↓
Similarity Search
   ↓
Relevant Chunks
   ↓
Text
   ↓
Prompt
   ↓
LLM
```

The vectors are primarily used to find the information.

The text is what is generally provided to the LLM as context.

---

# 32. Context + Question

The LLM needs both:

```text
Context
+
Question
```

Example:

```text
Context:
Customers may request a refund within 30 days.

Question:
What is the refund policy?
```

The context tells the LLM:

> What information should I use?

The question tells the LLM:

> What should I answer?

---

# 33. RAG = Retrieval + Augmentation + Generation

Break the name down:

### Retrieval

```text
Question
 ↓
Retrieve Relevant Chunks
```

### Augmentation

```text
Question
+
Retrieved Context
```

### Generation

```text
Context + Question
 ↓
LLM
 ↓
Answer
```

Therefore:

```text
Retrieval
    +
Augmentation
    +
Generation
    =
RAG
```

---

# 34. Complete RAG Architecture

```text
                         DOCUMENTS
                            │
                            ▼
                         Chunking
                            │
                            ▼
                          Chunks
                            │
                            ▼
                     Embedding Model
                            │
                            ▼
                         Vectors
                            │
                            ▼
                     Vector Database
                            │
                            │
                    ────────┼────────
                            │
                            ▲
                       User Question
                            │
                            ▼
                     Embedding Model
                            │
                            ▼
                     Question Vector
                            │
                            ▼
                     Similarity Search
                            │
                            ▼
                     Relevant Chunks
                            │
                            ▼
                Question + Retrieved Context
                            │
                            ▼
                           LLM
                            │
                            ▼
                         Answer
```

---

# 35. Where Do Tokens Fit?

Tokens are involved when models process text.

For ingestion:

```text
Chunk
 ↓
Tokenizer
 ↓
Tokens / Token IDs
 ↓
Embedding Model
 ↓
Vector
```

For a query:

```text
Question
 ↓
Tokenizer
 ↓
Tokens / Token IDs
 ↓
Embedding Model
 ↓
Question Vector
```

Tokens are not the same thing as embeddings.

---

# 36. Don't Let These Become Blurred Again

This is one of the most important sections of this lesson.

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
Numerical array representing the embedding
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

### Compact version

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

# 37. The Three Most Important Jobs

## Embedding Model

Answers:

> How can I represent this text numerically for semantic comparison?

```text
Text → Vector
```

---

## VectorDB

Answers:

> Which stored vectors are most similar to this query vector?

```text
Query Vector → Similar Vectors
```

---

## LLM

Answers:

> Given this context and question, what should I say?

```text
Context + Question → Answer
```

---

# 38. RAG Is Not Fine-Tuning

RAG does not retrain the LLM.

RAG:

```text
External Knowledge
      ↓
Retrieve at Query Time
      ↓
Provide as Context
```

Fine-tuning:

```text
Training Data
      ↓
Training Process
      ↓
Model Weights Change
```

They solve different problems.

---

# 39. RAG vs Fine-Tuning

### RAG

Useful when information:

* Changes frequently
* Is private
* Lives in external documents
* Needs retrieval
* Is too large to include in every prompt

### Fine-Tuning

Useful for modifying model behavior/style/patterns rather than simply supplying a changing knowledge base.

---

# 40. Why Retrieval Quality Matters

A powerful LLM cannot answer correctly from information that was never retrieved.

```text
Bad Retrieval
     ↓
Bad Context
     ↓
Potentially Bad Answer
```

Therefore RAG quality depends on more than the LLM.

It also depends on:

* Chunking
* Embedding model
* Retrieval strategy
* Metadata filtering
* Top-K selection
* Query transformation
* Context construction

---

# 41. RAG and Runnables

From R07 we learned:

```text
Question
   ↓
RunnableParallel
   ├── Retriever
   └── RunnablePassthrough
   ↓
Prompt
   ↓
Model
   ↓
Parser
```

Now we understand the Retriever:

```text
Question
   ↓
Retriever
   ↓
Embedding
   ↓
Vector Search
   ↓
Relevant Chunks
```

Therefore:

```text
Question
   │
   ▼
RunnableParallel
   │
   ├───────────────┐
   ▼               ▼
Retriever      Passthrough
   │               │
   ▼               ▼
Vector Search   Question
   │               │
   ▼               │
Relevant Chunks    │
   │               │
   └───────┬───────┘
           ▼
         Prompt
           ↓
         Model
           ↓
        Parser
           ↓
        Answer
```

This connects R07 and R08.

---

# 42. Storage Architecture

A VectorDB does not necessarily need to be the canonical source of application data.

For example:

```text
PostgreSQL
   ↓
Canonical Application Data
```

and:

```text
VectorDB
   ↓
Semantic Retrieval Index
```

A system may use both.

Another option is:

```text
VectorDB
 ├── Vector
 ├── Text
 └── Metadata
```

The correct architecture depends on application requirements.

---

# 43. Best Practices

## 1. Don't Chunk Blindly

Consider:

* Document structure
* Paragraphs
* Sections
* Sentences
* Tables
* Headers

---

## 2. Preserve Metadata

Useful metadata:

```text
document_id
page_number
section
community_id
document_type
```

---

## 3. Keep Access to Source Text

Unless there is a deliberate architectural reason not to, keep access to the original chunk text.

This makes:

* Retrieval
* Debugging
* Citations
* Auditing

easier.

---

## 4. Choose Chunk Size Experimentally

There is no universal perfect chunk size.

Evaluate:

* Retrieval precision
* Retrieval recall
* Context size
* Answer quality

---

## 5. Don't Retrieve Everything

Use:

```text
Top-K
```

and metadata filters when appropriate.

---

## 6. Don't Treat VectorDB as Automatically the Source of Truth

The VectorDB is often optimized for semantic retrieval.

Canonical application data may live in PostgreSQL or another primary data store.

---

## 7. Protect Access During Retrieval

For applications with user-specific/private documents, retrieval should respect:

```text
Authentication
Authorization
Metadata Filters
Community / Tenant Access
Document Permissions
```

Never assume that because a vector is semantically similar, the user is allowed to see its source content.

---

# 44. Mentor Questions

### Q1

What is a chunk?

### Q2

What is the difference between a token and a chunk?

### Q3

What is an embedding?

### Q4

Are embeddings human-readable?

### Q5

What is a Vector Database?

### Q6

How can a VectorDB return text if it searches vectors?

### Q7

What happens during ingestion?

### Q8

What happens during retrieval?

### Q9

What is a Retriever?

### Q10

What is the difference between a Retriever and a VectorDB?

### Q11

Why do we need chunking?

### Q12

Why is chunk overlap sometimes useful?

### Q13

Why do we embed the user question?

### Q14

Is RAG the same as fine-tuning?

### Q15

Why don't we send the entire document to the LLM?

---

# 45. Mini Challenge

Suppose:

```text
HOA_Bylaws.pdf
```

contains:

```text
500 pages
```

We split it into:

```text
2,000 chunks
```

and create embeddings for every chunk.

A user asks:

> "When must the annual meeting be held?"

Explain this flow:

```text
HOA_Bylaws.pdf
      ↓
   Chunks
      ↓
  Embeddings
      ↓
  VectorDB
```

Then:

```text
User Question
      ↓
      ?
      ↓
Relevant Chunks
      ↓
      ?
      ↓
LLM
      ↓
Answer
```

Answer:

1. Why don't we send all 2,000 chunks to the LLM?
2. What happens to the user's question before similarity search?
3. What exactly is being compared during vector search?
4. What does the Retriever return?
5. Why do we still send the original question along with the retrieved chunks to the LLM?
6. Where do tokens appear in this process?
7. Are chunks, tokens, embeddings, and vectors the same thing?

---

# 46. Final Mental Model

## Ingestion

```text
Document
   ↓
Chunking
   ↓
Chunks
   ↓
Tokenizer
   ↓
Tokens / Token IDs
   ↓
Embedding Model
   ↓
Embedding Vectors
   ↓
VectorDB
```

## Retrieval

```text
User Question
   ↓
Tokenizer / Model Processing
   ↓
Embedding Model
   ↓
Question Vector
   ↓
Similarity Search
   ↓
Top-K Relevant Chunks
```

## Generation

```text
Relevant Chunks
       +
Original Question
       ↓
     Prompt
       ↓
      LLM
       ↓
    Answer
```

---

# 47. One-Line Summary

> **RAG retrieves relevant chunks from an external knowledge source using vector similarity, adds those chunks to the user's question as context, and gives the combined information to an LLM to generate an answer.**

---

## Connections

Previous:

* **R07 – Runnables & LCEL**

Current:

* **R08 – RAG Fundamentals**

Next:

* **R09 – Practical RAG Pipeline**

---

# Final Cheat Sheet

```text
DOCUMENT
   ↓
CHUNK
   ↓
TOKENIZE
   ↓
TOKENS / TOKEN IDs
   ↓
EMBEDDING MODEL
   ↓
VECTOR
   ↓
VECTORDB
```

Query:

```text
QUESTION
   ↓
EMBEDDING
   ↓
QUESTION VECTOR
   ↓
SIMILARITY SEARCH
   ↓
TOP-K CHUNKS
```

Generation:

```text
QUESTION
   +
RETRIEVED CHUNKS
   ↓
PROMPT
   ↓
LLM
   ↓
ANSWER
```

Remember:

```text
Chunk       → Piece of text
Token       → Tokenizer unit
Token ID    → Numeric token identifier
Embedding   → Semantic numerical representation
Vector      → Numerical representation/array
VectorDB    → Vector storage/search
Retriever   → Relevant document/chunk retrieval
Context     → Information given to LLM
LLM         → Generates answer
```
