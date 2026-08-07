# 2 – Tokens

Computers process numbers, not text. Before an LLM can run, text is split into **tokens** and mapped to integer IDs.

## Why not characters or whole words?

**Characters** (`H e l l o`) create too many steps and weak language structure.

**Whole words** explode vocabulary size (`understanding`, `understood`, `understandable`, …). Tokenizers split text into reusable pieces instead (`Play` + `ing`).

## What is a token?

The **smallest unit** an LLM processes. It can be a word, part of a word, punctuation, a space, or an emoji. **One word is not always one token.**

## Tokenizer

A tokenizer turns text into token IDs:

```
"I love Python" → ["I", " love", " Python"] → [40, 1842, 11321]
```

The model works on those IDs—not the original string.

## Pipeline

```
Text → Tokenizer → Token IDs → Embedding layer → Embeddings → Transformer → Next token
```

## Token ≠ embedding

| Token / Token ID | Embedding |
|------------------|-----------|
| Integer identifier | Dense float vector |
| From the tokenizer | Semantic representation for the Transformer |

Token IDs become embeddings; they are not the same thing. Vector databases store **embeddings** (often with original text), not raw token IDs.

## Why tokens matter

They drive context-window size, prompt length, API cost, streaming, chunk sizing, and RAG limits. Different models can use different tokenizers.

## Common misconceptions

- One word ≠ one token
- Tokens ≠ embeddings (tokens *become* embeddings)
- Models don't all tokenize the same way
- The LLM predicts the **next token**, not "words" as such

## Practice

See [p01_tokens.py](p01_tokens.py) (`tiktoken` encode / count).

## Interview questions

- What is a token?
- Are words and tokens the same?
- Are tokens stored in a vector database? (No—embeddings are.)

## Summary

LLMs never consume raw text. A tokenizer produces token IDs; those become embeddings; the model then predicts one token at a time.
