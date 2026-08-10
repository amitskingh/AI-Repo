# 7 – Embeddings

## Why Do Embeddings Exist?

Computers cannot naturally determine that:

```text
"I love Python."

"Python is my favorite programming language."

"I really enjoy programming in Python."
```

have similar meanings.

Humans can recognize the relationship easily.

Embeddings provide a way to represent text numerically so that relationships between pieces of data can be measured mathematically.

## What Is an Embedding?

An embedding is a **numerical vector representation** produced by an embedding model.

Example:

```text
"I love Python."

        ↓

Embedding Model

        ↓

[0.21, -0.83, 0.45, 0.12, ...]
```

This list of numbers is called a **vector**.

The vector can contain hundreds or thousands of dimensions depending on the embedding model.

## What Is a Vector?

For now, think of a vector as:

> **A list of numbers representing some data.**

Example:

```python
vector = [
    0.21,
    -0.83,
    0.45,
    0.12,
]
```

The individual numbers should NOT be interpreted as simple human-readable properties.

Do not assume:

```text
0.21 = Python
-0.83 = Programming
0.45 = Positive
```

That is not how embeddings work.

The useful information is distributed across the vector.

## Token vs Chunk vs Embedding

These are three different concepts.

### Token

A token is a unit of text processed by a language model.

```text
"Python"

↓

Token ID

↓

11321
```

### Chunk

A chunk is a piece of a larger document.

```text
PDF
 ↓
Chunk 1
Chunk 2
Chunk 3
```

Chunks are still text.

### Embedding

An embedding is a numerical representation of text.

```text
Chunk

↓

Embedding Model

↓

[0.21, -0.83, 0.45, ...]
```

## Pipeline

Conceptually:

```text
Document
    ↓
Split into Chunks
    ↓
Chunk Text
    ↓
Embedding Model
    ↓
Vector
    ↓
Vector Database
```

Internally, the embedding model may tokenize the text:

```text
Chunk
  ↓
Tokenizer
  ↓
Token IDs
  ↓
Embedding Model
  ↓
Vector
```

Therefore, we normally don't manually think of the pipeline as:

```text
Chunk → Token → Embedding
```

Instead:

```text
Chunk → Embedding Model → Vector
```

The tokenization is handled internally.

## What Does Semantic Mean?

**Semantic = related to meaning.**

Therefore:

> **Semantic similarity = similarity in meaning.**

Example:

```text
"The dog is sleeping."

"The puppy is resting."
```

These sentences use different words but describe a similar situation.

Therefore:

```text
High Semantic Similarity
```

Compare:

```text
"The dog is sleeping."

"The database query failed."
```

These have very different meanings.

Therefore:

```text
Low Semantic Similarity
```

## How Embeddings Capture Relationships

Imagine a mathematical space.

```text
                 Programming
                      ●
                    /   \
                   /     \
              Python     Java
                 ●         ●

        Weather
           ●
```

Related concepts can occupy nearby regions.

This allows us to compare representations mathematically.

Important:

The embedding does NOT contain an explicit dictionary like:

```text
0.25 = programming
0.71 = Python
```

Instead, relationships are represented across the entire vector space.

## Semantic Search

Traditional keyword search may struggle with:

```text
Query:
"What maintenance does a car need?"

Document:
"Automobiles require regular maintenance."
```

The exact words are different:

```text
car ≠ automobile
```

But their meanings are related.

Embeddings allow us to search based on semantic relationships.

```text
Question
   ↓
Embedding Model
   ↓
Question Vector
   ↓
Similarity Search
   ↓
Relevant Document Vector
   ↓
Original Text
```

## Vector Database

A Vector Database stores and searches vectors efficiently.

A stored record may look conceptually like:

```python
{
    "embedding": [0.21, -0.83, 0.45, ...],
    "text": "Automobiles require regular maintenance.",
    "metadata": {"page": 12, "document": "manual.pdf"},
}
```

The embedding is used for searching.

The original text is returned for the LLM.

## Similarity

Two vectors are not normally compared using exact equality.

For example:

```text
A = [0.20, 0.80, 0.40]

B = [0.21, 0.79, 0.42]
```

They may represent similar content.

We therefore need mathematical methods to measure similarity.

Common methods include:

* Cosine Similarity
* Euclidean Distance
* Dot Product

We will study these mathematically in **Module 7 – Vector Databases**.

## Cosine Similarity – Intuition

Cosine similarity looks at the **direction** of vectors.

Imagine:

```text
       B
      /
     /
    /
   /____ A
```

If vectors point in similar directions:

```text
High Similarity
```

If they point in very different directions:

```text
Low Similarity
```

The exact mathematics will be covered later.

## Embeddings Are Not Just for Words

Embeddings can represent different types of data:

* Words
* Sentences
* Paragraphs
* Document chunks
* Code
* Images
* Audio

The general idea is:

```text
Data
 ↓
Embedding Model
 ↓
Vector
```

## Embedding Model vs LLM Embedding Layer

These should not be confused.

### Embedding Model

Used externally for tasks such as:

```text
Document
   ↓
Embedding Model
   ↓
Vector
   ↓
Vector DB
```

This is commonly used in RAG.

### LLM Embedding Layer

Inside a language model:

```text
Text
 ↓
Tokenizer
 ↓
Token IDs
 ↓
Embedding Layer
 ↓
Transformer
```

Both involve numerical representations, but their purposes are different.

## Complete RAG Connection

We can now connect the concepts learned so far.

### Ingestion

```text
PDF
 ↓
Split into Chunks
 ↓
Embedding Model
 ↓
Vectors
 ↓
Vector DB
```

### Retrieval

```text
User Question
 ↓
Embedding Model
 ↓
Question Vector
 ↓
Vector DB
 ↓
Similarity Search
 ↓
Relevant Text Chunks
 ↓
LLM
 ↓
Answer
```

This is the foundation of semantic retrieval in RAG.

## Common Misconceptions

#### Token = Embedding

No.

```text
Token
 ↓
Token ID / model input unit
```

while:

```text
Embedding
 ↓
Numerical vector representation
```

#### Chunk = Token

No.

A chunk is a larger piece of text.

A chunk can contain many tokens.

```text
Chunk
 ↓
Many Tokens
```

#### Vector DB understands language

Not directly.

The embedding model creates numerical representations.

The Vector DB performs efficient mathematical search over those vectors.

#### One embedding number represents one meaning

No.

The information is distributed across the vector.

#### Embeddings are human-readable meanings

No.

You generally cannot look at:

```text
[0.21, -0.83, 0.45, ...]
```

and interpret the individual values directly.

## Best Practices

#### Use the Same Embedding Model

Use the same embedding model for documents and queries.

```text
Documents
   ↓
Embedding Model A

Questions
   ↓
Embedding Model A
```

This keeps both representations in the same vector space.

#### Store Useful Metadata

Example:

```python
{"page": 42, "document": "bylaws.pdf", "community_id": 123}
```

Metadata can later be used to filter retrieval.

#### Don't Assume Larger Dimensions = Better

A higher-dimensional embedding is not automatically better.

Embedding quality depends on:

* Embedding model
* Dataset
* Task
* Retrieval strategy

## Interview questions

- What is an embedding?
- What is semantic similarity?
- What is the difference between a token and an embedding?
- Why are embeddings useful in RAG?
- Does each embedding dimension have a human-readable meaning?

## Summary

Embeddings convert data into numerical vectors that allow relationships between pieces of data to be measured mathematically.

The key idea is:

```text
Text
 ↓
Embedding Model
 ↓
Vector
 ↓
Similarity Search
 ↓
Relevant Information
```

This is the foundation of semantic search and one of the core building blocks of RAG.

```

#### Your mental model after R07

You should now be able to distinguish these clearly:

```text
CHUNK
"A car requires regular maintenance."
        ↓
      TEXT

TOKEN
"car"
        ↓
    Token ID

EMBEDDING
[0.12, -0.83, 0.44, ...]
        ↓
Numerical representation

VECTOR DB
        ↓
Stores/searches vectors
```

And the overall RAG relationship:

```text
Document
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector DB
   ↓
Semantic Search
   ↓
Relevant Chunks
   ↓
LLM
```

## Key takeaways

* Embeddings are numerical vector representations.
* A vector is a list of numbers.
* Embedding values are not individually human-readable meanings.
* Semantic means related to meaning.
* Embeddings enable semantic similarity search.
* Chunks are text; embeddings are vectors.
* Tokens and embeddings are different.
* Vector databases search embeddings and return associated data.
* Embeddings are fundamental to modern RAG systems.

## New terminology

| Term                | Meaning                                           |
| ------------------- | ------------------------------------------------- |
| Embedding           | Numerical vector representation                   |
| Vector              | List of numerical values                          |
| Semantic            | Related to meaning                                |
| Semantic Similarity | Similarity in meaning                             |
| Embedding Model     | Model that converts data into vectors             |
| Vector Database     | Database optimized for vector search              |
| Cosine Similarity   | Similarity based on vector direction              |
| Euclidean Distance  | Straight-line distance between vectors            |
| Dot Product         | Mathematical operation used for vector comparison |

## Connections

Previous:

* **R06 – Prompt Engineering**

Current:

* **R07 – Embeddings**

Next:

* **R08 – Transformers**

