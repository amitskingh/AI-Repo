# 4 – Temperature

Temperature controls **how randomly** the LLM picks the next token during inference. It does not change knowledge, training, or "intelligence."

## Mental model

Suppose next-token probabilities are:

| Token | Probability |
|--------|------------:|
| Python | 90% |
| Java | 8% |
| Rust | 2% |

- **Low temperature** → almost always `Python`
- **High temperature** → more chance of `Java` / `Rust` (more variety, less predictability)

## Typical scale

| Temperature | Behaviour |
|-------------|-----------|
| 0.0 | Deterministic |
| 0.2 | Stable |
| 0.5 | Balanced |
| 0.7 | Conversational |
| 1.0+ | Creative / less predictable |

## When to use what

| Task | Temperature |
|------|-------------|
| RAG, SQL, JSON, legal/medical | 0.0 |
| Code | 0–0.2 |
| Summarization | 0.2–0.4 |
| Chat | 0.5–0.7 |
| Brainstorming / creative writing | 0.8–1.0 |

Low values favor consistency and accuracy. High values favor creativity and exploration.

## LangChain example

```python
model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
)
```

## Common misconceptions

- Higher temperature ≠ smarter model
- Temperature only affects **inference** sampling, not training

## Interview questions

- What is temperature?
- Does it affect model knowledge? (No.)
- Preferred temperature for RAG? (0 or near 0.)

## Summary

Temperature tunes randomness of next-token selection. It shapes predictability vs creativity—not how much the model knows.
