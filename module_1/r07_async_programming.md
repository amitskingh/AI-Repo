# 7 – Asynchronous Programming

AI apps spend much of their time **waiting**—LLM APIs, vector DBs, databases, network I/O. Async lets Python do other work during those waits instead of blocking the thread.

## Sync vs async waiting

Synchronous flow:

```
LLM → wait → DB → wait → vector search → wait → done
```

Most of that wall-clock time is idle. Async asks: *can I make progress on something else while waiting?*

## Concurrency vs parallelism

| Concurrency | Parallelism |
|-------------|-------------|
| Many tasks make progress over the same period | Tasks run at the same time |
| Often one thread + switching | Needs multiple cores/threads |

**Async is about waiting efficiently** (concurrency). Parallelism is about using multiple processors.

## Coroutines and `await`

```python
async def greet(): ...
```

Calling `greet()` returns a **coroutine object**—nothing runs yet. Execution starts when you `await` it (or schedule it on the event loop).

`await` pauses the **current coroutine**, not the whole thread. The event loop can run other ready coroutines meanwhile.

```python
await asyncio.sleep(2)  # pause this coroutine; loop keeps working
time.sleep(2)  # blocks the entire thread / event loop
```

## Event loop

The event loop is the scheduler: run a ready task, and when it hits `await`, switch to another. Python typically switches only at suspension points (`await`). Code between two `await`s runs continuously on one thread.

## Concurrent tasks

```python
# Sequential — ~4s if each takes 2s
await fetch_user()
await fetch_documents()

# Concurrent — ~2s
await asyncio.gather(fetch_user(), fetch_documents())
```

`gather` still usually uses **one thread**. Only one coroutine runs Python bytecode at a time; the loop switches when one awaits.

## Common mistakes

- `time.sleep()` inside async code — freezes the event loop; use `await asyncio.sleep()`
- Thinking async means multiple threads — usually one thread, many coroutines
- Calling `task()` without `await` — creates a coroutine; does not run it

## AI / LangChain connection

| Sync | Async |
|------|-------|
| `invoke()` | `ainvoke()` |
| `stream()` | `astream()` |
| `batch()` | `abatch()` |

Same APIs; async variants keep the event loop free while waiting on the model or tools.

## Core idea

> At `await`, a coroutine voluntarily yields control back to the event loop.

## Interview questions

- What is async? What is a coroutine?
- Concurrency vs parallelism? `time.sleep` vs `asyncio.sleep`? What does `await` do?
- How does the event loop work? Why doesn't `gather` create multiple threads? When can the loop switch?

## Summary

Async uses waiting time productively by switching coroutines instead of blocking. LLM apps are I/O-bound; understanding `await`, the event loop, and `gather` makes `ainvoke` / `astream` and concurrent agent work feel natural.
