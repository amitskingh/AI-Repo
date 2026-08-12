# 7 – Runnables & LCEL

## Learning Objectives

After completing this lesson, I should be able to:

- Explain what a Runnable is.
- Understand why LangChain components can be composed together.
- Explain LCEL.
- Understand the `|` pipe operator.
- Understand `RunnableSequence`.
- Understand `RunnableLambda`.
- Understand `RunnablePassthrough`.
- Understand `RunnableParallel`.
- Understand `RunnableBranch`.
- Understand `invoke()`, `batch()`, and `stream()`.
- Understand how Runnables are useful for RAG.
- Understand why `RunnablePassthrough` is not Memory.
- Understand how Runnables differ from Tools, Memory, and Context.

---

# 1. What Is a Runnable?

A Runnable is a LangChain component that can be executed with an input and produce an output.

Simple mental model:

```text
Input
  ↓
Runnable
  ↓
Output
```

A Runnable can be thought of as a composable LEGO block.

For example:

```text
Prompt
Model
Parser
Python Function
Retriever
```

can participate in Runnable-based workflows.

---

# 2. Why Do We Need Runnables?

Different LangChain components perform different jobs.

```text
Prompt
 ↓
creates model input

Model
 ↓
generates response

Parser
 ↓
transforms response
```

Runnables provide a common composable execution model so these components can be connected.

Instead of manually coordinating every component, we can compose them:

```python
chain = prompt | model | parser
```

---

# 3. Runnable Mental Model

Think of every Runnable as:

```text
Input
  ↓
┌─────────────┐
│  Runnable   │
└─────────────┘
  ↓
Output
```

The important idea is:

> A Runnable is a composable unit of execution.

It is not limited to an LLM.

---

# 4. Runnables Are Not Only LLMs

A Runnable can represent different types of work:

```text
Prompt
Model
Parser
Retriever
Python Function
Routing Logic
Other Runnable Components
```

Therefore:

```text
Runnable
    ≠
LLM
```

Runnable is a broader abstraction.

---

# 5. You've Already Used Runnables

Examples:

```python
prompt.invoke(...)
```

```python
model.invoke(...)
```

```python
parser.invoke(...)
```

These components can participate in the Runnable system.

This is one reason we can write:

```python
prompt | model | parser
```

---

# 6. LCEL

LCEL stands for:

> **LangChain Expression Language**

It provides syntax and abstractions for composing LangChain Runnables.

Example:

```python
chain = prompt | model | parser
```

Mental model:

```text
LCEL
 ↓
Composition of Runnables
```

---

# 7. The Pipe Operator `|`

The pipe operator means:

> Pass the output of one Runnable into the next Runnable.

For example:

```python
prompt | model
```

means:

```text
Prompt Output
     ↓
Model Input
```

And:

```python
prompt | model | parser
```

means:

```text
Prompt
  ↓
Model
  ↓
Parser
```

---

# 8. RunnableSequence

When Runnables are composed sequentially:

```python
chain = prompt | model | parser
```

the workflow behaves like a sequence.

Conceptually:

```text
RunnableSequence
├── Prompt
├── Model
└── Parser
```

Execution:

```text
Input
 ↓
Prompt
 ↓
Model
 ↓
Parser
 ↓
Output
```

---

# 9. Manual Execution vs Composition

Without composition:

```python
x = prompt.invoke(
    {
        "topic": "RAG"
    }
)

y = model.invoke(x)

z = parser.invoke(y)
```

With LCEL:

```python
chain = prompt | model | parser

result = chain.invoke(
    {
        "topic": "RAG"
    }
)
```

Both represent the same conceptual flow.

LCEL provides a cleaner compositional approach.

---

# 10. Runnable Input and Output

Different Runnables can have different input and output types.

For example:

```text
Dictionary
    ↓
Prompt
    ↓
PromptValue
    ↓
Model
    ↓
AIMessage
    ↓
Parser
    ↓
String
```

Therefore, the output of one Runnable becomes the input of the next compatible Runnable.

---

# 11. RunnableLambda

`RunnableLambda` allows a normal Python function to participate in a Runnable workflow.

Import:

```python
from langchain_core.runnables import RunnableLambda
```

Example:

```python
def double(x):
    return x * 2

double_runnable = RunnableLambda(double)

result = double_runnable.invoke(5)

print(result)
```

Result:

```text
10
```

Flow:

```text
5
 ↓
RunnableLambda
 ↓
double()
 ↓
10
```

Mental model:

> `RunnableLambda` = turn my Python function into a Runnable.

---

# 12. Why RunnableLambda Is Useful

It allows application-specific Python logic to participate in a chain.

Example:

```text
Prompt
 ↓
Model
 ↓
Your Python Function
 ↓
Parser
```

For example:

```python
def add_prefix(text):
    return f"Answer: {text}"

prefix = RunnableLambda(add_prefix)
```

Then:

```python
chain = prompt | model | StrOutputParser() | prefix
```

Your own Python function becomes part of the Runnable workflow.

---

# 13. Application Code vs LangChain

Important distinction:

> **Application means your application code.**

For example:

```python
def check_balance(user_id):
    ...
```

is your application logic.

LangChain can orchestrate when the function participates in a workflow, but the function itself remains application code.

---

# 14. RunnablePassthrough

`RunnablePassthrough` passes its input through unchanged.

Example:

```python
from langchain_core.runnables import RunnablePassthrough

passthrough = RunnablePassthrough()

result = passthrough.invoke("Hello")

print(result)
```

Result:

```text
Hello
```

Flow:

```text
"Hello"
   ↓
RunnablePassthrough
   ↓
"Hello"
```

---

# 15. Why Do We Need RunnablePassthrough?

It is not required because Python cannot preserve variables.

We could simply write:

```python
question = "What is RAG?"

context = retriever.invoke(question)

data = {
    "context": context,
    "question": question,
}
```

That is perfectly valid.

The value of `RunnablePassthrough` is that it lets the original input participate directly in a Runnable composition.

---

# 16. RunnablePassthrough in a Composition

Suppose:

```text
Question
   │
   ├──→ Retriever
   │
   └──→ Passthrough
```

The Retriever transforms the question into context.

The Passthrough preserves the original question.

Result:

```python
{
    "context": [...],
    "question": "What is RAG?"
}
```

The important idea:

> `RunnablePassthrough` does not store the value. It simply passes the current input through unchanged.

---

# 17. RunnablePassthrough Is NOT Memory

Very important:

```text
RunnablePassthrough
    ≠
Memory
```

RunnablePassthrough:

```text
Current Input
     ↓
Same Input
```

Memory:

```text
Previous Information
     ↓
Store / Retrieve
     ↓
Available Later
```

Passthrough does not remember conversations.

---

# 18. RunnableParallel

`RunnableParallel` sends the same input to multiple Runnable branches.

Example:

```python
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

def double(x):
    return x * 2

def square(x):
    return x * x

double_runnable = RunnableLambda(double)
square_runnable = RunnableLambda(square)

parallel = RunnableParallel(
    double=double_runnable,
    square=square_runnable,
)
```

Invoke:

```python
result = parallel.invoke(5)
```

Conceptually:

```python
{
    "double": 10,
    "square": 25
}
```

---

# 19. RunnableParallel Visualized

```text
                 5
              /     \
             ↓       ↓
          double   square
             ↓       ↓
            10       25
              \     /
               \   /
                ↓
        {
          double: 10,
          square: 25
        }
```

Mental model:

> `RunnableParallel` = same input → multiple branches → combined result.

---

# 20. RunnableSequence vs RunnableParallel

This distinction is very important.

## Sequence

```python
double_runnable | square_runnable
```

Flow:

```text
5
 ↓
double
 ↓
10
 ↓
square
 ↓
100
```

Output:

```text
100
```

The output of one becomes the input of the next.

---

## Parallel

```python
RunnableParallel(
    double=double_runnable,
    square=square_runnable
)
```

Flow:

```text
        5
       / \
      ↓   ↓
   double square
      ↓   ↓
     10   25
```

Output:

```python
{
    "double": 10,
    "square": 25
}
```

Remember:

```text
Sequence
→ output becomes next input

Parallel
→ same input goes to multiple branches
```

---

# 21. RunnableBranch

`RunnableBranch` allows conditional routing.

Conceptually:

```text
Input
  ↓
Condition
  ↓
┌───────────────┐
│               │
▼               ▼
True           False
│               │
▼               ▼
Path A         Path B
```

Example:

```python
from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
)

def positive(x):
    return "Positive"

def negative(x):
    return "Negative"

branch = RunnableBranch(
    (
        lambda x: x > 0,
        RunnableLambda(positive),
    ),
    RunnableLambda(negative),
)
```

Then:

```python
branch.invoke(5)
```

returns:

```text
Positive
```

And:

```python
branch.invoke(-5)
```

returns:

```text
Negative
```

Mental model:

> `RunnableBranch` = choose a workflow based on a condition.

---

# 22. Four Important Runnable Concepts

| Runnable              | Meaning                                    |
| --------------------- | ------------------------------------------ |
| `RunnableLambda`      | Run your Python function                   |
| `RunnablePassthrough` | Pass input unchanged                       |
| `RunnableParallel`    | Run multiple branches using the same input |
| `RunnableBranch`      | Choose a path based on a condition         |
| `RunnableSequence`    | Execute components sequentially            |

---

# 23. `invoke()`

The most basic execution method is:

```python
result = runnable.invoke(input)
```

Meaning:

> Execute this Runnable with this input.

Example:

```python
result = chain.invoke(
    {
        "topic": "RAG"
    }
)
```

Mental model:

```text
One Input
   ↓
invoke()
   ↓
One Result
```

---

# 24. `batch()`

`batch()` allows multiple inputs to be passed through a Runnable.

Example:

```python
inputs = [
    {"topic": "RAG"},
    {"topic": "Embeddings"},
    {"topic": "Vector DB"},
]

results = chain.batch(inputs)
```

Mental model:

```text
Input 1 ─┐
Input 2 ─┼→ Chain → Results
Input 3 ─┘
```

Do not think of `batch()` as automatically guaranteeing parallel execution in every implementation. The actual execution/concurrency behavior can depend on the Runnable implementation and configuration.

---

# 25. `stream()`

`stream()` allows results to be consumed incrementally when the Runnable supports streaming.

Example:

```python
for chunk in chain.stream(input):
    print(chunk)
```

Mental model:

```text
LLM
 ↓
Chunk
 ↓
Chunk
 ↓
Chunk
 ↓
Final Output
```

This is useful for chat interfaces where the user should see the response progressively.

---

# 26. Three Important Execution Methods

For now remember:

```text
invoke()
    ↓
One input → One result

batch()
    ↓
Many inputs → Many results

stream()
    ↓
Incremental output
```

Async variants also exist, such as:

```python
await chain.ainvoke(input)
```

For now, focus on the conceptual difference.

---

# 27. Runnables and RAG

Runnables become particularly useful when constructing RAG workflows.

Suppose:

```text
Question
```

needs to be sent to a Retriever.

The Retriever returns:

```text
Relevant Chunks
```

But we also need the original question.

So:

```text
                    Question
                   /        \
                  /          \
                 ↓            ↓
            Retriever     Passthrough
                 ↓            ↓
             Chunks        Question
                 \            /
                  \          /
                   ↓        ↓
                     Prompt
                       ↓
                     Model
                       ↓
                    Parser
                       ↓
                    Answer
```

This is a major RAG composition pattern.

---

# 28. RunnableParallel + RunnablePassthrough for RAG

Conceptually:

```python
chain = RunnableParallel(
    context=retriever,
    question=RunnablePassthrough(),
)
```

Input:

```text
"What is RAG?"
```

Output:

```python
{
    "context": [
        "Relevant chunk 1...",
        "Relevant chunk 2..."
    ],
    "question": "What is RAG?"
}
```

Then this dictionary can be sent to the Prompt.

---

# 29. Why Preserve the Original Question?

The Retriever needs the question to find relevant chunks.

But the LLM also needs the original question to know what it should answer.

For example:

```text
Context:
Customers can request a refund within 30 days.

Question:
What is the refund policy?
```

The Retriever gives:

```text
Context
```

The Passthrough preserves:

```text
Question
```

Then:

```text
Context + Question
       ↓
Prompt
       ↓
LLM
```

Therefore:

> The Retriever finds relevant information, while the LLM uses that information to answer the original question.

---

# 30. `RunnablePassthrough` vs Python Variable

Both approaches are valid.

### Normal Python

```python
question = "What is RAG?"

context = retriever.invoke(question)

data = {
    "context": context,
    "question": question,
}
```

### Runnable Composition

```python
RunnableParallel(
    context=retriever,
    question=RunnablePassthrough(),
)
```

The difference is that the second approach expresses the data flow as part of the Runnable graph.

`RunnablePassthrough` is therefore a **composition tool**, not a storage mechanism.

---

# 31. Complete Conceptual RAG Chain

Eventually:

```python
chain = (
    RunnableParallel(
        context=retriever,
        question=RunnablePassthrough(),
    )
    | prompt
    | model
    | StrOutputParser()
)
```

Architecture:

```text
Question
   │
   ▼
RunnableParallel
   │
   ├───────────────┐
   ▼               ▼
Retriever      Passthrough
   │               │
   ▼               ▼
Chunks          Question
   │               │
   └───────┬───────┘
           ▼
        Prompt
           ↓
         Model
           ↓
        Parser
           ↓
        Answer
```

This is a real RAG composition pattern.

---

# 32. Runnables vs Memory

Do not confuse them.

```text
Runnable
→ Execute/compose operations

Memory
→ Retain/retrieve information
```

Example:

```text
Memory
 ↓
Previous Chat History
 ↓
Runnable
 ↓
Prompt
 ↓
Model
```

Runnable is responsible for execution/composition.

Memory is responsible for information retention/retrieval.

---

# 33. Runnables vs Context

```text
Runnable
→ Executable component/workflow

Context
→ Information supplied to the model
```

For example:

```text
Context:
Relevant document chunks

Runnable:
Prompt → Model → Parser
```

---

# 34. Runnables vs Tools

```text
Runnable
→ Composable execution abstraction

Tool
→ Capability that can be invoked
```

A Tool may participate in a Runnable-based workflow, but:

```text
Runnable ≠ Tool
```

---

# 35. Runnables vs Agents

A simple Runnable sequence might be:

```text
Prompt
 ↓
Model
 ↓
Parser
```

An Agent may involve:

```text
Model
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
Model
 ↓
Decision
 ↓
Tool
 ↓
Final Response
```

Agents introduce decision-making and potentially repeated tool interactions.

---

# 36. Runnables vs LangGraph

High-level distinction:

```text
Simple composition
        ↓
LangChain / LCEL / Runnables
```

More complex stateful workflows:

```text
State
 ↓
Node
 ↓
Decision
 ↓
Loop
 ↓
Tool
 ↓
Another Node
        ↓
LangGraph
```

We will study LangGraph separately.

---

# 37. Common Mistakes

### ❌ Runnable means LLM.

No.

Runnable is a broader composable execution abstraction.

---

### ❌ RunnablePassthrough stores data.

No.

It passes the current input unchanged.

---

### ❌ RunnableParallel means sequential execution.

No.

Parallel creates multiple processing branches from the same input.

---

### ❌ RunnableLambda is LangChain's business logic.

No.

It allows your own Python function to participate in the Runnable workflow.

---

### ❌ `batch()` always means parallel execution.

Not necessarily.

It represents batch execution through the Runnable interface; actual concurrency depends on implementation/configuration.

---

### ❌ Runnable is Memory.

No.

```text
Runnable → execution/composition
Memory → retention/retrieval
```

---

### ❌ Runnable is Context.

No.

```text
Runnable → executable component
Context → information supplied to the model
```

---

### ❌ Runnable is Tool.

No.

```text
Runnable → composable execution
Tool → capability/action
```

---

# 38. Best Practices

## 1. Keep Components Small

Prefer:

```text
Prompt
 ↓
Model
 ↓
Parser
```

over one giant function.

---

## 2. Use Composition

Prefer:

```python
chain = prompt | model | parser
```

when it clearly represents the workflow.

---

## 3. Keep Business Logic in Application Code

Important rules such as:

```text
Authorization
Balance checks
Community ownership
Permission checks
Confirmation
```

should remain enforceable by application code.

Do not rely solely on prompts or LLM decisions.

---

## 4. Use `RunnableLambda` for Small Custom Transformations

For example:

```python
RunnableLambda(clean_text)
```

Avoid turning one chain into a giant collection of unrelated application logic.

---

## 5. Use Parallel Branches When Appropriate

If two operations depend on the same input but not on each other's results:

```text
Input
 /   \
A     B
```

can be a good fit for `RunnableParallel`.

---

## 6. Use Streaming for User-Facing Responses

Streaming can improve perceived responsiveness in chat applications.

---

# 39. Mentor Questions

## Q1

What is a Runnable?

## Q2

Why can we write:

```python
prompt | model | parser
```

?

## Q3

What does LCEL stand for?

## Q4

What is the difference between:

```python
chain.invoke(...)
```

and:

```python
chain.batch(...)
```

?

## Q5

What does `RunnableLambda` allow us to do?

## Q6

What does `RunnablePassthrough` do?

## Q7

Why is `RunnablePassthrough` useful in a RAG workflow?

## Q8

What is the difference between:

```text
Runnable
Memory
Context
Tool
```

?

---

# 40. Mini Challenge

Suppose:

```text
question = "What is the refund policy?"
```

and we have:

```text
retriever
```

which returns:

```text
[
    "Refunds are available within 30 days.",
    "Refunds require the original receipt."
]
```

We want:

```python
{
    "context": [...],
    "question": "What is the refund policy?"
}
```

The architecture is:

```text
                    Question
                   /        \
                  ↓          ↓
             Retriever   Passthrough
                  │          │
                  ↓          ↓
               Chunks     Question
                  \          /
                   ↓        ↓
                     Prompt
                       ↓
                      Model
                       ↓
                     Parser
```

Questions:

1. Which Runnable should represent the retriever branch?
2. Which Runnable preserves the original question?
3. Which Runnable allows both branches to receive the same question?
4. What component receives the resulting dictionary next?
5. What should happen after the Chat Model if a plain string is required?

---

# 41. Answers to the Mini Challenge

### Q1

The Retriever itself can participate in the Runnable workflow.

If custom Python similarity-search logic is needed, it could also be wrapped with `RunnableLambda`.

```text
Question
 ↓
Retriever
 ↓
Relevant Chunks
```

---

### Q2

```python
RunnablePassthrough()
```

It preserves the original question.

---

### Q3

```python
RunnableParallel(...)
```

It sends the same input to both branches.

---

### Q4

The resulting dictionary goes to the Prompt.

```text
RunnableParallel
 ↓
Prompt
 ↓
Model
```

---

### Q5

Use:

```python
StrOutputParser()
```

```text
Model
 ↓
StrOutputParser
 ↓
String
```

---

# 42. Final Mental Model

```text
                    Runnable
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    Sequence        Parallel          Branch
       │               │                │
       ▼               ▼                ▼
    A → B → C       A + B          Condition
                                      ↓
                                    A / B
```

Helper Runnables:

```text
RunnableLambda
    ↓
Run my Python function

RunnablePassthrough
    ↓
Pass input unchanged
```

---

# 43. The RAG Connection

Everything we have learned is now connecting:

```text
User Question
      │
      ▼
   Retriever
      │
      ▼
Relevant Chunks
      │
      ├───────────────┐
      │               │
      ▼               ▼
   Context        Original Question
      │               │
      └───────┬───────┘
              ▼
           Prompt
              ↓
            Model
              ↓
           Parser
              ↓
           Answer
```

The next lesson will connect this workflow to the concepts you already learned earlier:

```text
Documents
   ↓
Chunks
   ↓
Tokens
   ↓
Embeddings
   ↓
Vectors
   ↓
Vector Database
   ↓
Similarity Search
   ↓
Retriever
   ↓
RAG Chain
```

---

# 44. Key Takeaways

* A Runnable is a composable unit of execution.
* Runnables are not limited to LLMs.
* LCEL means LangChain Expression Language.
* The `|` operator composes compatible Runnables.
* `RunnableSequence` represents sequential execution.
* `RunnableLambda` allows your Python functions to participate in the workflow.
* `RunnablePassthrough` passes the current input unchanged.
* `RunnablePassthrough` is not Memory and does not store information.
* `RunnableParallel` sends the same input through multiple branches.
* `RunnableBranch` chooses a path based on a condition.
* `invoke()` executes one input.
* `batch()` processes multiple inputs.
* `stream()` provides incremental output when supported.
* Runnables can be used to construct RAG workflows.
* In RAG, the Retriever finds relevant chunks while the original question is preserved for the final prompt.
* The Retriever's job is retrieval; the LLM's job is to use the retrieved context to answer the question.
* Runnables, Memory, Context, and Tools are different concepts.

---

# 45. One-Line Summary

> **Runnables are composable units of execution, and LCEL allows us to connect them into clean workflows such as Prompt → Model → Parser or Retriever + Question → Prompt → Model → Answer.**

---

## Connections

Previous:

* **R06 – Output Parsers & Structured Output**

Current:

* **R07 – Runnables & LCEL**

Next:

* **R08 – RAG: Retriever, Chunks, Embeddings & Vector Database**

---

# Final Mental Model to Memorize

```text
Input
  │
  ▼
Runnable
  │
  ├── Sequence
  │      ↓
  │    A → B → C
  │
  ├── Parallel
  │      ↓
  │    A + B
  │
  ├── Branch
  │      ↓
  │    A / B
  │
  ├── Lambda
  │      ↓
  │    Your Python Function
  │
  └── Passthrough
         ↓
      Same Input
```

For RAG:

```text
Question
   │
   ▼
RunnableParallel
   │
   ├──→ Retriever → Relevant Chunks
   │
   └──→ Passthrough → Original Question
                     │
                     ▼
                   Prompt
                     ↓
                   Model
                     ↓
                  Parser
                     ↓
                  Answer
```
