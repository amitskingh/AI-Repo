# 3 – Type Hints

Python is dynamically typed: a variable can hold any type. That flexibility hurts maintainability in large apps. Type hints make code self-documenting and let tools catch mistakes before runtime.

LangChain, FastAPI, and Pydantic all rely heavily on type hints.

## Why they exist

```python
def process(data):  # what is data?
    ...


def process(data: str) -> str:  # input and output are clear
    ...
```

Hints improve readability, tooling, and communication. They are **metadata**—Python does not enforce them at runtime (unless another library does).

## How Python stores them

```python
def greet(name: str) -> str:
    return f"Hello {name}"


greet.__annotations__
# {"name": str, "return": str}
```

Frameworks read `__annotations__`. That is how FastAPI builds docs, Pydantic validates input, and LangChain builds tool schemas.

## Syntax

```python
def greet(name: str) -> str:
    return f"Hello {name}"


age: int = 25
scores: list[int]
prices: dict[str, float]
nickname: str | None  # prefer over Optional[str] on 3.10+
value: int | float
operation: Callable[[int, int], int]  # from collections.abc
```

Prefer built-in generics (`list[str]`) over `typing.List` on Python 3.9+. Avoid `Any` unless you truly cannot be more specific.

## Static checkers, not runtime

```python
calculate("abc", "xyz")  # Python allows this
```

Tools like mypy, pyright, and Pylance will warn. Frameworks that *do* validate (Pydantic, FastAPI) use the hints at runtime.

## Best practices

- Type every parameter and return value
- Prefer `str | None` over `Optional[str]` (3.10+)
- Prefer precise types over `Any`

## Common mistakes

- Assuming hints enforce types at runtime — they don't (by themselves)
- Overusing `Any`
- Omitting return types

## AI / LangChain connection

```python
@tool
def search(query: str, limit: int) -> str: ...
```

LangChain reads the annotations into a tool schema the LLM can call. Weak hints → weak schemas.

## Interview questions

- What are type hints? Why use them?
- Do they enforce types?
- `Optional[str]` vs `str | None`? `Any` vs `object`?
- How do FastAPI / LangChain use annotations?

## Summary

Type hints are metadata that IDEs, checkers, and frameworks use to understand your code. They are a core part of modern Python—and of every serious AI stack.
