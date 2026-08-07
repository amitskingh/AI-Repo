# 5 – Top-p (Nucleus Sampling)

Top-p keeps the smallest set of tokens whose **cumulative probability** reaches `p`, then samples from that set. Unlikely tokens in the long tail are dropped. That core set is the **nucleus**—hence "nucleus sampling."

## Example

Next-token probabilities:

| Token | Probability | Cumulative |
|--------|------------:|-----------:|
| Python | 50% | 50% |
| Java | 20% | 70% |
| Rust | 15% | 85% |
| Go | 10% | 95% |
| COBOL | 3% | — |
| Brainfuck | 2% | — |

With `top_p = 0.90`, candidates stop once cumulative ≥ 0.90 → Python, Java, Rust, Go. The rest are discarded.

## Temperature vs Top-p

| Temperature | Top-p |
|-------------|-------|
| How random is selection? | Who is allowed to be selected? |
| Reshapes / softens probabilities | Filters the candidate pool |

## LangChain example

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.7,
    top_p=0.9,
)
```

## Practical defaults

| Task | Temperature | Top-p |
|------|-------------|-------|
| RAG / code / JSON | 0 | 1 |
| General chat | ~0.7 | 1 |
| Brainstorming | ~0.9 | ~0.95 |
| Story writing | ~1 | ~0.9 |

Most production systems (RAG, agents, SQL, structured output) use `temperature=0` and leave `top_p=1`. Prefer tuning **temperature** first; avoid changing both unless you know why.

## Common mistakes

- Treating Top-p and Temperature as the same
- Assuming lower Top-p makes the model smarter (it only shrinks the pool)
- Always tuning both at once

## Interview questions

- What is Top-p?
- How does it differ from temperature?
- Which is tuned more often? (Temperature; Top-p often stays at default.)

## Summary

Top-p filters low-probability tokens before sampling. Temperature controls randomness within (or after reshaping) that process. In production, temperature is the usual knob; Top-p is often left alone.
