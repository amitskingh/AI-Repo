# Module 2 – LLM Fundamentals

Core ideas behind Large Language Models—what they are, how text becomes tokens, what limits a single request, and how sampling parameters shape output.

This module sits between Python essentials and framework-heavy work (LangChain, RAG, agents). After it, concepts like context limits, token cost, temperature, and retrieval should feel concrete—not magical.

## Learning objectives

By the end of this module you should be able to:

- Explain what an LLM is and how it generates text token by token
- Distinguish tokens, token IDs, and embeddings
- Explain context windows, why RAG exists, and where memory lives
- Choose sensible Temperature and Top-p values for different tasks

## Prerequisites

- [Module 1 – Python Essentials](../module_1/README.md)
- No prior ML or LangChain experience required

## Roadmap

```
LLM → Tokens → Context Window → Temperature → Top-p
```

## Contents

| Note | Topic | Practice |
|------|--------|----------|
| [r01_llms.md](r01_llms.md) | What is an LLM? | — |
| [r02_tokens.md](r02_tokens.md) | Tokens | [p01_tokens.py](p01_tokens.py) |
| [r03_context_window.md](r03_context_window.md) | Context window | — |
| [r04_temperature.md](r04_temperature.md) | Temperature | — |
| [r05_top_p.md](r05_top_p.md) | Top-p (nucleus sampling) | — |

## How to use

1. Read each note in order.
2. Run the practice file and experiment with different strings.
3. Use the interview questions at the end of each note for self-check.
