# 1 – What is a Large Language Model (LLM)?

An LLM is a trained machine learning model that predicts the **next token** from previous tokens. It does not think like a human—it follows learned statistical patterns.

## Why LLMs exist

Rule-based chatbots don't scale:

```python
if user_input == "Hi":
    ...
elif user_input == "Hello":
    ...
```

Users ask the same thing in countless ways. LLMs learn patterns from large datasets instead of hand-written rules.

## How text is generated

```
Prompt → Tokenizer → Tokens → Predict next token → Append → Repeat → Response
```

Responses are built **one token at a time**, not all at once.

## What "Large Language Model" means

| Word | Meaning |
|------|---------|
| **Large** | Huge datasets, billions of parameters, massive compute |
| **Language** | Text and code forms: English, Python, SQL, JSON, Markdown, … |
| **Model** | A trained system that makes predictions |

## Training vs inference

| Training | Inference |
|----------|-----------|
| Data → learning → model | Prompt → model → response |
| Rare, expensive, GPU-heavy | Every user request (e.g. ChatGPT) |

## Common misconceptions

- LLMs don't "understand" like humans—they predict tokens.
- They don't emit a full paragraph at once—they emit one token at a time.

## Production connection

Every LangChain app eventually calls an LLM:

```python
response = model.invoke("Explain decorators.")
```

LangChain orchestrates the workflow; the LLM generates the text.

## Interview questions

- What is an LLM?
- Does an LLM understand language? (No—it predicts tokens from learned patterns.)

## Summary

An LLM is a predictive model trained on massive data. It generates responses by repeatedly predicting the next token until the output is complete.
