# Module 1 – Python Essentials for AI Engineering

Master the Python concepts that power LangChain, LangGraph, FastAPI, Pydantic, and modern AI applications.

This is **not** a full Python course. It covers only the features you will repeatedly encounter in AI frameworks—enough to understand *why* they exist and *how* they show up in real systems.

## Learning objectives

By the end of this module you should be able to:

- Write reusable functions and design classes with clear responsibilities
- Read and write modern Python with type hints
- Choose dataclasses vs normal classes appropriately
- Explain decorators, generators (`yield`), and async/`await`
- Isolate project dependencies with virtual environments

## Prerequisites

- Variables, loops, conditionals, and basic Python syntax
- No prior AI, LangChain, or LLM experience required

## Why this module exists

LangChain code often looks like magic until you know the underlying Python:

```python
from langchain_core.tools import tool


@tool
def calculator(a: int, b: int) -> int:
    return a + b
```

Decorators, type hints, and functions explain `@tool`. Likewise, `await model.ainvoke(prompt)` only makes sense once you know async. This module removes that magic.

## Roadmap

```
Functions → Classes → Type Hints → Dataclasses
    → Decorators → Generators → Async → Virtual Environments
```

## Contents

| Note | Topic | Practice |
|------|--------|----------|
| [r01_functions.md](r01_functions.md) | Functions | — |
| [r02_classes.md](r02_classes.md) | Classes | [p01_class.py](p01_class.py) |
| [r03_type_hints.md](r03_type_hints.md) | Type hints | [p02_typehints.py](p02_typehints.py) |
| [r04_dataclasses.md](r04_dataclasses.md) | Dataclasses | [p03_dataclasses.py](p03_dataclasses.py), [p04_dataclasses_chatbot.py](p04_dataclasses_chatbot.py) |
| [r05_decorators.md](r05_decorators.md) | Decorators | [p05_decorators.py](p05_decorators.py) |
| [r06_generators.md](r06_generators.md) | Generators | [p06_generators.py](p06_generators.py) |
| [r07_async_programming.md](r07_async_programming.md) | Async programming | [p07_async_programming.py](p07_async_programming.py) |
| [r08_virtual_environments.md](r08_virtual_environments.md) | Virtual environments | — |

## How to use

1. Read each note in order.
2. Run the matching practice file(s) and experiment.
3. Use interview questions at the end of each note for self-check.
