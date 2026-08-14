# 10 – Retrieval Quality & Advanced Retrieval

## Learning Objectives

After completing this lesson, I should be able to:

- Understand why basic vector retrieval is not always sufficient.
- Understand Top-K retrieval.
- Understand similarity thresholds.
- Understand metadata filtering.
- Understand why similarity does not equal authorization.
- Understand query rewriting.
- Understand query decomposition.
- Understand multi-query retrieval.
- Understand hybrid search.
- Understand reranking.
- Understand two-stage retrieval.
- Understand parent-child retrieval.
- Understand contextual compression.
- Understand retrieval precision and recall.
- Understand how to debug retrieval separately from generation.
- Understand how production RAG systems improve retrieval quality.

---

# 1. Retrieval Is Not Automatically Good

A basic RAG system can work like:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Top-K
   ↓
LLM
```

But:

> **Top-K does not automatically mean Top-K relevant chunks.**

For example:

```text
Question:
"What is the annual meeting requirement?"
```

Vector search may return:

```text
Chunk A → 0.91
Chunk B → 0.89
Chunk C → 0.87
Chunk D → 0.84
```

But these might represent:

```text
A → Annual meeting requirements
B → Board meeting requirements
C → Meeting notice requirements
D → Annual meeting expenses
```

They are all related to meetings, but they aren't equally useful.

Therefore:

```text
High Similarity
      ≠
Perfect Relevance
```

---

# 2. Why Can Retrieval Be Wrong?

Poor retrieval can result from:

* Poor chunking
* Poor embedding model
* Ambiguous query
* Too many results
* Too few results
* Missing metadata filters
* Similar but irrelevant chunks
* Poor query formulation

Conceptually:

```text
Poor Chunking
     ↓
Poor Retrieval
     ↓
Poor Context
     ↓
Poor Answer
```

---

# 3. Retrieval Quality Has Multiple Layers

Think of retrieval as a pipeline:

```text
                    Retrieval Quality
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
    Chunking          Embeddings        Retrieval
        ↓                 ↓                 ↓
    Good pieces       Good vectors      Good ranking
```

Additional factors include:

```text
Metadata
Query Design
Top-K
Similarity Threshold
Hybrid Search
Reranking
```

---

# 4. Top-K

Example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
```

`k=5` means:

> Retrieve the top 5 results.

Conceptually:

```text
10,000 chunks
      ↓
Similarity Search
      ↓
Top 5
```

But some of those five may not actually be relevant.

---

# 5. Too Small a K

Suppose:

```text
k = 1
```

But answering the question requires:

```text
Chunk A → Meeting date
Chunk B → Notice requirements
Chunk C → Voting requirements
```

Retrieving only one chunk may produce:

```text
Too Small K
    ↓
Missing Context
    ↓
Incomplete Answer
```

---

# 6. Too Large a K

Suppose:

```text
k = 50
```

We may retrieve:

```text
50 chunks
```

This can cause:

* More tokens
* Higher cost
* More irrelevant information
* Larger prompts
* More context noise

Therefore:

```text
Too Large K
    ↓
Retrieval Noise
    ↓
Larger Prompt
```

---

# 7. There Is No Universal K

Don't memorize:

```text
k = 5
```

as a universal rule.

The correct value depends on:

* Document type
* Chunk size
* Question complexity
* Retrieval strategy
* Context window
* LLM
* Application requirements

The correct approach is:

> **Tune K using evaluation.**

---

# 8. Similarity Threshold

Suppose search produces:

```text
Chunk A → 0.94
Chunk B → 0.91
Chunk C → 0.88
Chunk D → 0.42
Chunk E → 0.19
```

We could use a threshold such as:

```text
threshold = 0.80
```

Then:

```text
A → ✅
B → ✅
C → ✅
D → ❌
E → ❌
```

This prevents clearly unrelated chunks from entering the context.

---

# 9. Similarity Scores Are Not Universal

A score such as:

```text
0.85
```

does NOT universally mean:

> "85% relevant."

The meaning of the score depends on:

* Embedding model
* Similarity metric
* Vector store
* Normalization
* Retrieval implementation

Therefore:

> Don't blindly compare similarity scores across different systems.

---

# 10. Top-K + Threshold

These can be combined.

```text
10,000 chunks
      ↓
Similarity Search
      ↓
Top 10
      ↓
Threshold Filter
      ↓
3 Useful Chunks
```

This can be better than blindly passing all 10 results to the LLM.

---

# 11. Metadata Filtering

Metadata filtering is one of the most important retrieval techniques.

Suppose we have:

```text
Community A
Community B
Community C
```

and the user belongs to:

```text
Community B
```

Instead of:

```text
All Documents
   ↓
Similarity Search
```

we can do:

```text
User
 ↓
Community B Filter
 ↓
Similarity Search
 ↓
Relevant Community B Chunks
```

---

# 12. Why Metadata Filtering Matters

Example:

```python
metadata = {
    "community_id": 102,
    "document_type": "bylaws",
    "year": 2026,
    "page": 42
}
```

Metadata can help with:

* Filtering
* Authorization boundaries
* Source tracking
* Citations
* Debugging
* Document types
* Dates
* Versions

---

# 13. Metadata Filtering Is Not Just Retrieval Optimization

Metadata can also enforce application constraints.

For example:

```text
community_id = 102
year = 2026
document_type = "bylaws"
```

This means the semantic search happens within the appropriate scope.

Conceptually:

```text
All Chunks
    ↓
Metadata Constraints
    ↓
Allowed Candidate Set
    ↓
Semantic Search
```

---

# 14. Retrieval + Authorization

This is extremely important.

Suppose a private document gets a high similarity score.

That does NOT mean the user is allowed to see it.

Therefore:

```text
Similarity
    ≠
Authorization
```

A safer conceptual architecture is:

```text
User
 ↓
Authentication
 ↓
Authorization
 ↓
Allowed Scope
 ↓
Metadata Filtering
 ↓
Retrieval
 ↓
Relevant Chunks
```

Never use semantic similarity as an access-control mechanism.

---

# 15. Query Rewriting

Users don't always formulate questions in an ideal retrieval format.

Example:

> "Can you please look through everything and tell me according to our latest bylaws when we're supposed to have the annual meeting?"

A query-rewriting step could produce:

```text
"2026 annual meeting date according to bylaws"
```

Flow:

```text
Original Question
      ↓
Query Rewriter
      ↓
Better Search Query
      ↓
Retriever
```

---

# 16. Why Query Rewriting?

Users may use:

* Conversational language
* Unnecessary instructions
* Long background information
* Ambiguous wording
* Pronouns
* References to previous conversation

Example:

> "What about the thing we discussed earlier regarding the meeting?"

The Retriever may not understand what "the thing" means.

A query transformation step can turn it into a more explicit search query.

---

# 17. Query Decomposition

Some questions contain multiple information needs.

Example:

> "When is the annual meeting, who receives notice, and what happens if notice isn't provided?"

We can decompose it into:

```text
Query 1:
"When is the annual meeting?"

Query 2:
"Who must receive meeting notice?"

Query 3:
"What happens if meeting notice isn't provided?"
```

Then:

```text
Query 1 → Chunks A, B
Query 2 → Chunks C, D
Query 3 → Chunks E, F
```

This is called:

> **Query Decomposition**

---

# 18. Multi-Query Retrieval

Sometimes different wordings can retrieve different relevant information.

Example:

```text
Original:
"How much can the HOA fine me?"
```

Possible search queries:

```text
"What is the maximum HOA fine?"
"HOA fine limits"
"association fine amount"
"violation penalty limit"
```

Conceptually:

```text
Original Question
      ↓
Multiple Search Queries
   /      |       \
  Q1      Q2       Q3
   \      |       /
    \     |      /
     Relevant Chunks
```

---

# 19. Hybrid Search

Vector search is not always enough.

For example:

> "What does section 720.303 say?"

Exact keyword matching can be extremely useful for:

```text
720.303
```

A better system may combine:

```text
Semantic Search
+
Keyword Search
```

This is called:

> **Hybrid Search**

---

# 20. Semantic Search vs Keyword Search

## Keyword Search

Looks for lexical/exact matches.

Example:

```text
"720.303"
```

is useful when the query contains:

```text
720.303
```

---

## Semantic Search

Looks for meaning.

Example:

```text
"How often must the association hold meetings?"
```

may retrieve text discussing:

```text
annual meetings
```

even when the exact phrase isn't present.

---

# 21. Hybrid Search Architecture

```text
                 Query
                   │
          ┌────────┴────────┐
          ↓                 ↓
   Keyword Search     Semantic Search
          ↓                 ↓
       Results A          Results B
          \                 /
           \               /
            ↓             ↓
             Combine/Rank
                  ↓
            Final Results
```

Hybrid search is especially useful for:

* Legal documents
* Technical documentation
* Product catalogs
* IDs
* Statutes
* Exact terminology

---

# 22. Reranking

Suppose initial retrieval produces:

```text
Question
   ↓
Vector Search
   ↓
Top 20 Candidates
```

Instead of sending all 20 to the LLM:

```text
Top 20
   ↓
Reranker
   ↓
Top 5
   ↓
LLM
```

A reranker evaluates the relationship between:

```text
Question
+
Candidate Chunk
```

and produces a better ordering.

---

# 23. Retriever vs Reranker

Do not confuse them.

### Retriever

```text
Find candidate documents
```

### Reranker

```text
Reorder candidate documents based on relevance
```

Example:

```text
Retriever:
A, B, C, D, E

Reranker:
C, A, E, B, D
```

The reranker generally doesn't discover completely new documents.

It improves the ordering of candidates.

---

# 24. Two-Stage Retrieval

A common architecture:

```text
Stage 1
───────
Fast Retrieval
     ↓
Top 20 / Top 50

Stage 2
───────
Reranking
     ↓
Top 3 / Top 5
```

Why?

Because expensive reranking across millions of documents would be inefficient.

So:

```text
Broad + Fast
      ↓
Narrow + Precise
```

---

# 25. Parent-Child Retrieval

Sometimes small chunks are excellent for finding relevant information but too small to provide enough context.

Example:

```text
Parent Section
├── Child A
├── Child B
├── Child C
└── Child D
```

Search:

```text
Question
   ↓
Child B
   ↓
Parent Section
   ↓
Larger Context
```

This is useful when:

> Small chunks retrieve well, but larger context is needed for answering.

---

# 26. Contextual Compression

Suppose a retrieved chunk contains:

```text
500 words
```

but only:

```text
80 words
```

are relevant.

A compression step can extract the useful portion.

```text
Retrieved Chunk
      ↓
Compression
      ↓
Relevant Portion
      ↓
LLM
```

This can reduce unnecessary context.

---

# 27. Advanced Retrieval Pipeline

A mature RAG system might look like:

```text
Question
   ↓
Query Rewrite
   ↓
Metadata Filter
   ↓
Hybrid / Semantic Search
   ↓
Top 20 Candidates
   ↓
Reranker
   ↓
Top 5
   ↓
Context Compression
   ↓
Prompt
   ↓
LLM
```

Not every application needs every stage.

> **Add complexity only when it solves a measured problem.**

---

# 28. Retrieval Evaluation

We need to determine whether retrieval is actually good.

Suppose:

```text
Question:
"When must the annual meeting be held?"
```

Expected relevant chunk:

```text
Chunk A
```

Retriever returns:

```text
Chunk A
Chunk B
Chunk C
```

Now we can evaluate whether the relevant information was retrieved.

---

# 29. Recall

Simplified definition:

> **Did we retrieve the relevant information?**

If the correct chunk is:

```text
Chunk A
```

and we retrieved:

```text
A, B, C
```

then recall is good.

If we retrieved:

```text
B, C, D
```

then recall is poor because A was missed.

---

# 30. Precision

Simplified definition:

> **How much of what we retrieved was actually relevant?**

Suppose:

```text
Retrieved:
A, B, C, D, E
```

and only:

```text
A, B
```

are relevant.

Precision is lower.

If:

```text
Retrieved:
A, B
```

and both are relevant:

```text
Precision is higher.
```

---

# 31. Recall vs Precision

Think:

```text
High Recall
→ Find more relevant information
→ May retrieve more noise
```

```text
High Precision
→ Less noise
→ May miss useful information
```

A good RAG system balances both.

---

# 32. Retrieval vs Generation Evaluation

A bad final answer can come from two different problems.

## Retrieval Problem

```text
Correct information
was never retrieved.
```

## Generation Problem

```text
Correct information
was retrieved,
but the LLM used it incorrectly.
```

Therefore debug in this order:

```text
Question
   ↓
Did retrieval find the right chunks?
   ↓
YES
   ↓
Inspect prompt/context
   ↓
Did the LLM use the context correctly?
```

---

# 33. Example: Retrieval Failure

Question:

> "What is the annual meeting date?"

Retriever returns:

```text
Parking rules
Pool maintenance
Vendor requirements
```

No annual meeting information was retrieved.

Potential fixes:

```text
Better Chunking
Better Embeddings
Query Rewrite
Metadata Filtering
Hybrid Search
Different K
Reranking
```

---

# 34. Example: Retrieval Is Good

Question:

> "What is the annual meeting date?"

Retriever returns:

```text
Chunk A:
Board meeting procedures.

Chunk B:
Parking regulations.

Chunk C:
Annual meeting is scheduled for April 15.
```

Chunk C is highly relevant.

Chunk A may be somewhat related.

Chunk B is irrelevant.

Possible improvements:

```text
Metadata
+
Reranking
+
Better K
```

---

# 35. Important Example: Similarity vs Relevance

Question:

> "What is the annual meeting date?"

Retrieved:

> "The association conducts annual meetings."

This is semantically relevant.

But:

> "The 2026 annual meeting is scheduled for April 15."

is much more useful.

Therefore:

```text
Similarity
    ≠
Relevance
```

---

# 36. Metadata + Semantic Search

A strong retrieval request can conceptually contain:

```python
{
    "query": "What is the annual meeting date?",
    "filter": {
        "community_id": 123,
        "year": 2026,
        "document_type": "bylaws"
    }
}
```

Now we have:

```text
Semantic Requirement
+
Structured Constraints
```

This is more powerful than pure semantic search.

---

# 37. Retrieval Hierarchy

Think of retrieval improvements as layers:

```text
Level 1
Basic Vector Search
        ↓
Level 2
Metadata Filtering
        ↓
Level 3
Query Rewriting / Multi-Query
        ↓
Level 4
Hybrid Search
        ↓
Level 5
Reranking
        ↓
Level 6
Compression / Parent Retrieval
```

Do not assume every project needs Level 6.

---

# 38. Best Practices

### 1. Start Simple

Begin with:

```text
Chunk
 ↓
Embed
 ↓
Retrieve
 ↓
Prompt
 ↓
LLM
```

Measure first.

---

### 2. Inspect Retrieved Chunks

Always inspect:

```text
Question
   ↓
Retrieved Chunks
```

before debugging the LLM.

---

### 3. Preserve Metadata

Useful metadata includes:

```text
tenant/community
document_id
page
section
version
document_type
```

---

### 4. Enforce Authorization

Do not assume:

```text
Similar
=
Allowed
```

Authorization must be enforced independently.

---

### 5. Tune Top-K

Don't blindly use:

```text
k = 5
```

for every application.

---

### 6. Use Similarity Thresholds Carefully

Similarity scores depend on the model and retrieval implementation.

---

### 7. Use Hybrid Search When Exact Terms Matter

Especially for:

```text
IDs
Section numbers
Statutes
Product codes
Names
Exact terminology
```

---

### 8. Use Reranking When Initial Retrieval Is Noisy

```text
Fast Retrieval
   ↓
Candidate Set
   ↓
Rerank
   ↓
Final Context
```

---

### 9. Evaluate Retrieval Separately

Don't only evaluate the final answer.

Also evaluate whether the correct information was retrieved.

---

# 39. Mini Challenge

Suppose the user asks:

> "According to the 2026 bylaws of Community A, when is the annual meeting and who must receive notice?"

VectorDB contains:

```text
Chunk A
community_id = A
year = 2026

"Annual meeting is scheduled for April 15, 2026."


Chunk B
community_id = B
year = 2026

"Annual meeting is scheduled for May 20, 2026."


Chunk C
community_id = A
year = 2026

"Notice must be provided to all eligible members."


Chunk D
community_id = A
year = 2025

"Annual meeting was scheduled for March 10, 2025."
```

### Questions

1. Which metadata filters should we apply?
2. Which chunks should ideally survive filtering?
3. Why is Chunk B dangerous even if it has high semantic similarity?
4. Why is Chunk D potentially dangerous?
5. Would you use only vector similarity, or combine it with metadata filtering?
6. If 20 chunks remain after filtering, what could you use to reduce them to the best 3–5 chunks?
7. Where does the LLM come into the process?

---

# 40. Mini Challenge Review

Correct reasoning:

### Q1

Use:

```text
community_id = A
year = 2026
```

Potentially additional filters:

```text
document_type = bylaws
version = latest
is_active = true
```

depending on the system.

---

### Q2

The metadata filter leaves:

```text
Chunk A
Chunk C
```

Both are valid candidates.

The semantic retrieval/reranking stage decides which is more relevant to the specific question.

---

### Q3

Chunk B belongs to another community.

Even if:

```text
similarity = 0.95
```

the user may not be authorized to see it.

```text
Similarity
≠
Authorization
```

---

### Q4

Chunk D is from 2025.

It may be semantically relevant but is not the requested 2026 information.

This demonstrates:

```text
Similarity
≠
Relevance
```

---

### Q5

Use both:

```text
Metadata Filtering
+
Semantic Search
```

Metadata constrains the search space while semantic retrieval finds information relevant to the question.

---

### Q6

Use:

```text
Reranker
```

Conceptually:

```text
20 Candidates
    ↓
Reranker
    ↓
Best 3–5
```

---

### Q7

The LLM comes after retrieval.

```text
Question
   ↓
Retrieval
   ↓
Relevant Chunks
   ↓
Context + Question
   ↓
Prompt
   ↓
LLM
   ↓
Answer
```

---

# 41. Don't Let These Become Blurred Again

This section is especially important.

```text
Chunk
→ Piece of original text
```

```text
Token
→ Unit produced by a tokenizer
```

```text
Token ID
→ Numeric identifier representing a token
```

```text
Embedding
→ Semantic numerical representation produced by an embedding model
```

```text
Vector
→ Numerical representation/array used for mathematical comparison
```

```text
VectorDB
→ Stores, indexes, and searches vectors
```

```text
Retriever
→ Retrieves relevant documents/chunks
```

```text
Reranker
→ Reorders retrieved candidates based on relevance
```

```text
Context
→ Information provided to the LLM
```

```text
LLM
→ Generates the final answer
```

---

## Three Critical Distinctions

### 1. Similarity ≠ Relevance

A chunk can be semantically similar but still not contain the answer.

```text
Similarity
    ↓
"Does this look related?"

Relevance
    ↓
"Does this actually help answer the question?"
```

---

### 2. Retrieval ≠ Generation

```text
Retriever
→ Finds evidence

LLM
→ Generates answer
```

---

### 3. Retriever ≠ VectorDB

```text
VectorDB
→ Storage/search infrastructure

Retriever
→ Higher-level interface that retrieves relevant documents
```

---

# 42. Final Mental Model

A basic RAG pipeline:

```text
Question
   ↓
Embedding
   ↓
Vector Search
   ↓
Top-K
   ↓
Context
   ↓
LLM
```

A better production-oriented retrieval pipeline:

```text
                    User Question
                          │
                          ▼
                    Query Analysis
                          │
                          ▼
                    Query Rewrite
                          │
                          ▼
                   Metadata Filter
                          │
                          ▼
              ┌───────────┴───────────┐
              ↓                       ↓
       Keyword Search          Vector Search
              ↓                       ↓
              └───────────┬───────────┘
                          ▼
                     Candidates
                          │
                          ▼
                       Reranker
                          │
                          ▼
                    Best Chunks
                          │
                          ▼
                   Context Builder
                          │
                          ▼
                       Prompt
                          │
                          ▼
                         LLM
                          │
                          ▼
                       Answer
```

But remember:

> **Not every production system needs every stage.**

Start simple, evaluate, identify the actual bottleneck, and then add complexity.

---

# 43. Final Principles

```text
Similarity does not mean authorization.

Similarity does not always mean relevance.

Retrieval does not generate the answer.

The LLM does not magically know which documents are relevant.

Metadata filtering narrows the allowed search space.

Reranking improves the ordering of retrieved candidates.

Top-K is a configuration, not a universal constant.

Retrieval quality and generation quality are separate problems.
```

---

# 44. One-Line Summary

> **Advanced RAG improves retrieval quality using techniques such as Top-K tuning, similarity thresholds, metadata filtering, query rewriting, query decomposition, hybrid search, reranking, parent retrieval, and context compression—while keeping authorization separate from semantic similarity.**

---

## Connections

Previous:

* **R09 – Practical RAG Pipeline**

Current:

* **R10 – Retrieval Quality & Advanced Retrieval**

Next:

* **R11 – RAG Evaluation & Production Considerations**
