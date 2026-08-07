# 3 – Context Window

A **context window** is the maximum number of **tokens** an LLM can process in a single request—not words or characters.

Think of a library (all knowledge) vs a small desk (what fits in one sitting). The desk is the context window.

## What shares the budget

Everything in one request competes for the same token limit:

- System prompt
- Chat history
- Current user question
- Retrieved documents
- Tool results

## Why RAG and chunking exist

A 500-page PDF may be hundreds of thousands of tokens. A model with a 128k window cannot take it all. Most of that text is irrelevant to one question anyway.

**Chunking** splits documents into smaller pieces of **text** (chunks are not tokens). **RAG** retrieves only the relevant chunks and places those into the context window.

```
PDF → Chunks → Embeddings → Vector DB
User question → Embedding → Similarity search → Relevant text chunks → LLM → Answer
```

## Context window vs memory

| Context window | Memory |
|----------------|--------|
| Temporary, one request | Outside the LLM |
| Hard token limit | Postgres, Redis, files, vector DB, … |

The LLM never "reads memory" directly. The app retrieves data and puts it into the context window. The model does not remember past chats unless the app re-sends them.

## PostgreSQL vs vector DB

| PostgreSQL (typical) | Vector DB (typical) |
|----------------------|---------------------|
| Users, chats, messages, metadata | Embeddings + text + metadata |
| CRUD, history, analytics | Semantic / similarity search for RAG |

Small chatbots may use Postgres alone. Semantic search usually needs both.

**Important:** similarity search uses embeddings; what gets sent to the LLM is usually the matched **text**, not the embedding vector.

## Common misconceptions

- Context window ≠ memory
- Vector DB returns text to the LLM (via retrieval), not raw embeddings as the answer payload
- Chunks are text pieces, not tokens
- The app remembers conversations; the LLM only sees the current window

## Interview questions

- What is a context window?
- Why does RAG exist?
- Does a vector DB return embeddings to the LLM? (No—associated text.)
- Does an LLM remember previous conversations? (No—the app must include them.)

## Summary

The context window is the LLM's fixed-size working area. RAG and external memory decide what text fits inside so the model can answer without overflowing the token budget.
