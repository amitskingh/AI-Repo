# 1 – Functions

Functions package logic into a reusable unit: receive input, do work, optionally return a result.

Without them, the same calculation gets copy-pasted everywhere:

```python
total = price * quantity
print(total)
```

Write it once, call it whenever needed:

```python
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity
```

## Syntax

| Piece | Role |
|-------|------|
| `def` | Defines a function |
| `calculate_total` | Name — describe *what* it does |
| `price: float` | Parameter with type hint |
| `-> float` | Expected return type |
| `return` | Sends a value back and exits |

## Prefer return over print

```python
def greet(name: str) -> str:
    return f"Hello, {name}"


message = greet("Harvey")
print(message)  # Hello, Harvey
```

Returning keeps the function reusable: print it, save it, send it to an API, or write it to a file without changing the function.

## Functions are objects

```python
def greet(): ...
```

creates a function object stored in memory. `greet` refers to the object; `greet()` executes it. That distinction matters for decorators.

## Best practices

- One responsibility per function
- Prefer returning values over printing
- Use descriptive names and type hints
- Keep functions short and focused

```python
# Good
def calculate_total(price: float, quantity: int) -> float:
    return price * quantity


# Bad — unclear names, no types
def calc(x, y):
    return x * y
```

## Common mistakes

**Printing instead of returning** — callers cannot reuse printed output.

**Too many responsibilities** — a function that validates payment, sends email, updates the DB, and prints an invoice should be split.

## AI / LangChain connection

Production AI apps are pipelines of small functions: `load_documents` → `split_text` → `generate_embeddings` → `retrieve` → `call_llm` → `format_response`.

`@tool` decorates a **function**. Solid function fundamentals make decorators much easier.

## Interview questions

- What is a function?
- Why is returning usually better than printing?
- Why are functions first-class objects in Python?

## Summary

Functions are reusable units of work. Well-designed ones are testable, readable, and maintainable—and they underpin tools, chains, and AI workflows.
