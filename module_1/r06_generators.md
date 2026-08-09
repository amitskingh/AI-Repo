# 6 – Generators

A normal function returns and discards its state. A generator **pauses** with `yield`, remembers where it stopped, and continues later—producing values one at a time (**lazy evaluation**). That is why generators are memory-efficient.

## The problem

```python
numbers = list(range(1, 1_000_001))  # all 1M ints in memory at once
```

A generator produces values only when asked:

```python
def numbers():
    for number in range(1, 1_000_001):
        yield number
```

## `return` vs `yield`

| `return` | `yield` |
|----------|---------|
| Ends the function | Pauses and resumes later |
| State is discarded | State is preserved |

```python
def greet():
    yield "Hello"
    yield "World"
```

Calling `greet()` does **not** run the body—it returns a generator object. Execution starts on `next()` (or a `for` loop).

```python
gen = greet()
next(gen)  # "Hello" — pause
next(gen)  # "World" — pause
next(gen)  # StopIteration
```

A `for` loop calls `next()` until `StopIteration`.

## Generator expressions

```python
numbers = [x * 2 for x in range(5)]  # list — all values now
numbers = (x * 2 for x in range(5))  # generator — lazy
```

## Common mistakes

- Expecting `numbers()` to run immediately — it only creates the generator
- Using `return` when you need multiple successive values — use `yield`
- Reusing an exhausted generator — create a new one; the second loop over the same object yields nothing

## AI / LangChain connection

```python
model.stream(...)  # tokens one by one (like a generator)
model.astream(...)  # async version of the same idea
```

Streaming LLM responses is the same mental model: pause, produce, resume.

## Core idea

> Generators pause execution while preserving state. Memory savings follow from that.

## Interview questions

- What is a generator? `return` vs `yield`?
- What happens on `next()`? Why are generators memory-efficient?
- Generator lifecycle? How does LangChain streaming relate?

## Summary

Generators produce values lazily while keeping execution state. Use them for large data, streaming, and any pipeline where you should not load everything into memory at once.
