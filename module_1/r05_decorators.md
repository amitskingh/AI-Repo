# 5 – Decorators

A decorator is a function that takes another function and returns a new function—usually wrapping extra behavior around the original.

Frameworks use them everywhere: FastAPI `@app.get()`, Flask `@app.route()`, Pytest `@pytest.mark`, LangChain `@tool`.

## The problem

You have many API handlers and need logging, timing, retries, or auth on all of them. Copy-pasting that into every function violates DRY. Decorators add behavior without rewriting each function.

## Build one by hand

```python
def logger(function):
    def wrapper():
        print("Function started")
        function()
        print("Function finished")
    return wrapper

def greet():
    print("Hello!")

greet = logger(greet)
greet()
# Function started
# Hello!
# Function finished
```

The `@` form is syntactic sugar for the same assignment:

```python
@logger
def greet():
    print("Hello!")
```

## Arguments and `functools.wraps`

Real decorators must accept any signature and preserve metadata:

```python
from functools import wraps

def logger(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Starting...")
        result = function(*args, **kwargs)
        print("Finished")
        return result
    return wrapper
```

Without `@wraps`, `greet.__name__` becomes `"wrapper"`. Always use it.

## Decorator factories

When the decorator itself needs parameters (`@retry(3)`), you nest three levels:

```python
def retry(max_attempts):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator
```

Python expands `@retry(3)` to `fetch_data = retry(3)(fetch_data)`:

1. `retry(3)` returns `decorator`
2. `decorator(fetch_data)` returns `wrapper`
3. Calls to `fetch_data()` run the wrapper (retry logic → original)

## Common mistakes

- Forgetting `return wrapper`
- Writing `def wrapper():` without `*args, **kwargs`
- Skipping `@wraps`

## AI / LangChain connection

```python
from langchain_core.tools import tool

@tool
def calculator(a: int, b: int) -> int:
    return a + b
```

`@tool` wraps your function, reads type hints, and builds a schema the LLM can call.

## Core idea

> A decorator receives a function and returns a new function.

Everything else builds on that.

## Interview questions

- What is a decorator? Why use one?
- How does `@decorator` work internally?
- Why `*args` / `**kwargs`? Why `functools.wraps`?
- Explain `@retry(3)` step by step. How does LangChain `@tool` use decorators?

## Summary

Decorators extend function behavior without changing the original implementation. Once you see the wrap-and-return pattern, FastAPI, Pytest, and LangChain decorators all look familiar.
