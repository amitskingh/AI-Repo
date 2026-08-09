# 2 – Classes

Functions handle individual tasks. Classes keep **related data and behavior** together.

LangChain, LangGraph, FastAPI, and Pydantic are built heavily around classes. Understanding them makes production AI code far easier to read.

## Why classes exist

A chatbot needs more than `reply(question)`. You also need history, model config, temperature, session ID, and so on. Passing all of that into every function gets messy fast.

Classes group:

- **State** — data belonging to the object
- **Behavior** — methods that operate on that data

A class is a **blueprint**; an object is an **instance** created from it. One class can create many independent objects.

## Constructor and `self`

`__init__` runs automatically when an object is created:

```python
class ChatBot:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def reply(self, question: str) -> str:
        return f"{self.model_name} received: {question}"


bot = ChatBot("GPT-4")
print(bot.reply("Explain decorators."))
# GPT-4 received: Explain decorators.
```

`self` is the current instance. Internally, `bot.reply(...)` is roughly `ChatBot.reply(bot, ...)`. Without `self`, Python would not know which object's data to use.

## Multiple objects

```python
bot1 = ChatBot("GPT-4")
bot2 = ChatBot("Claude")
bot1.model_name = "GPT-5"  # does not affect bot2
```

Each object has its own state.

## Instance vs class variables

```python
class ChatBot:
    company = "OpenAI"  # shared by all instances

    def __init__(self):
        self.history = []  # unique per instance
```

**Never** put a mutable default like `history = []` on the class unless you intentionally want every instance to share one list.

## Best practices

- One class, one responsibility (SRP)
- Meaningful names (`ChatHistory`, not `Data`)
- Focused methods (`reply()`, `clear_history()` — not `do_everything()`)

## Common mistakes

**Forgetting `self`** on methods → `TypeError`.

**Shared mutable state** on the class:

```python
# Wrong — one list for every instance
class ChatBot:
    history = []


# Correct
class ChatBot:
    def __init__(self):
        self.history = []
```

## AI / LangChain connection

Almost every LangChain component is a class/object:

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1")
```

`ChatOpenAI` is a class; `model` is an instance. Same pattern for prompts, documents, retrievers, and agents.

## Interview questions

- What is a class? An object? `self`?
- Class variable vs instance variable?
- Purpose of `__init__`? Why does Python pass `self` automatically?
- Object creation lifecycle (`__new__` → `__init__`)?
- When would you choose functions over classes?

## Summary

Classes combine state and behavior into reusable units. Modern AI frameworks are built around them—master this before diving into LangChain.
