# 1 – What is LangChain and Why Do We Need It?

## What Is LangChain?

LangChain is a framework for building applications powered by language models.

It provides components and abstractions for working with:

- Chat Models
- Prompts
- Messages
- Output Parsers
- Structured Output
- Tools
- Retrievers
- RAG
- Agents
- Streaming
- Runnables
- Chains

A simple mental model is:

```text
LangChain
    ↓
Framework for building LLM applications
```

## LangChain is not an LLM
This is one of the first things to remember.

LangChain is not:

```text
GPT
Claude
Gemini
Llama
```

Those are models.

Instead:

```text
LLM Provider
      ↓
     Model
```

while:

```text
LangChain
      ↓
Framework around models and application components
```

Conceptually:

```text
Your Application
       ↓
    LangChain
       ↓
      LLM
```

## Do We Need LangChain to Use an LLM?

No.

We can directly use a provider SDK.

For example, conceptually:

```python
response = model.invoke("Explain embeddings.")
```

or directly use the provider's own SDK.

LangChain is optional.

The purpose of LangChain is to make it easier to compose and manage more complex LLM application workflows.

## Why Do We Need LangChain?

A simple LLM application may look like:

```text
Prompt
  ↓
LLM
  ↓
Response
```

This is easy.

But a real AI application can become:

```text
Prompt
   ↓
Retriever
   ↓
Context
   ↓
Prompt
   ↓
LLM
   ↓
Tool
   ↓
Database
   ↓
LLM
   ↓
Structured Output
   ↓
Application
```

Managing all these components manually can become complicated.

LangChain provides reusable abstractions for composing these components.

## The Main Idea: Composition

The most important idea to remember is:

> **LangChain helps us compose LLM application components.**

For example:

```text
Prompt
   ↓
Model
   ↓
Parser
```

Or:

```text
Retriever
   ↓
Prompt
   ↓
Model
   ↓
Parser
```

Or eventually:

```text
User
   ↓
Agent
   ↓
Tool
   ↓
Retriever
   ↓
Model
   ↓
Structured Output
```

The components can be combined to create larger workflows.

## Simple LangChain Example

Conceptually:

```python
prompt = ChatPromptTemplate.from_template("Explain {topic}.")

chain = prompt | model

response = chain.invoke({"topic": "Python"})
```

The important part is:

```python
prompt | model
```

This represents composing two LangChain components.

Later we will learn **LCEL – LangChain Expression Language** in detail.

## LangChain Components

LangChain provides different building blocks.

### Chat Model

Used to interact with conversational LLMs.

```python
model = ChatOpenAI(...)
```

### Prompt Template

Creates reusable prompts.

```python
prompt = ChatPromptTemplate(...)
```

### Output Parser

Converts model output into a useful format.

```text
LLM Output
    ↓
Parser
    ↓
Python Data
```

### Runnable

A component that can be invoked and composed with other LangChain components.

Runnables are a fundamental concept behind LCEL.

### Chain

A sequence of connected components.

```text
Prompt
   ↓
Model
   ↓
Parser
```

### Retriever

Finds relevant documents.

```text
Question
   ↓
Retriever
   ↓
Relevant Documents
```

### Tool

Allows an LLM application to interact with external capabilities.

```text
LLM
 ↓
Tool
 ↓
API / Database / Service
```

## Simplified LangChain Architecture

```text
                         LangChain
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
     Prompts              Models                Tools
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                         Runnables
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
    Retrievers           Parsers              Agents
```

This is a simplified conceptual architecture, not an exact internal package diagram.

## LangChain Does Not Make the LLM Smarter

This is an important misconception to avoid.

LangChain does not automatically make an LLM:

* More intelligent
* More knowledgeable
* More accurate
* Less hallucination-prone

Instead:

```text
LLM
+
Application Architecture
+
LangChain Components
        ↓
LLM Application
```

The quality of the underlying model still matters.

## LangChain vs Direct Provider SDK

There are two approaches.

### Direct SDK

```text
Your Application
      ↓
Provider SDK
      ↓
LLM
```

Advantages can include:

* Direct access to provider features
* Less abstraction
* Simpler code for small applications
* Easier debugging in some cases

### LangChain

```text
Your Application
      ↓
LangChain
      ↓
Provider Model
```

Advantages can include:

* Reusable abstractions
* Standardized components
* Easier composition
* Tools
* Retrievers
* Chains
* Structured output integrations
* Streaming
* Runnable interfaces

The correct choice depends on the application.

## LangChain Is Not Mandatory

Do not develop the mindset:

```text
AI Application
    ↓
Must use LangChain
```

Instead:

```text
AI Application
    ↓
Choose appropriate tools
```

LangChain should be used when its abstractions provide value.

## LangChain vs LangGraph

These are related but different.

### LangChain

Think:

```text
Components
+
Composition
+
Pipelines
```

Example:

```text
Prompt
  ↓
Model
  ↓
Parser
```

### LangGraph

Think:

```text
State
+
Nodes
+
Edges
+
Loops
+
Control Flow
```

Example:

```text
       ┌─────────┐
       ↓         │
Start → Model → Tool
       ↑         │
       └─────────┘
```

LangGraph becomes especially useful for complex, stateful, multi-step workflows and agents.

We will learn LangGraph later.

## Why Learn LLM Fundamentals Before LangChain?

We already learned:

```text
Tokens
Context Window
Temperature
Top-p
Embeddings
Transformers
Tool Calling
Structured Output
```

These concepts are not replaced by LangChain.

Instead, LangChain provides abstractions around them.

For example:

```text
LLM Concept
     ↓
Underlying Model/API
     ↓
LangChain Abstraction
     ↓
Application
```

Therefore:

> **Don't use LangChain as a black box.**

Understand what happens underneath.

## Connection With Python Fundamentals

The Python concepts learned earlier now become useful.

For example:

```python
@tool
def search(query: str) -> str: ...
```

This contains:

```text
Decorator
Function
Type Hint
      ↓
LangChain Tool
```

Similarly:

```python
async def main(): ...
```

becomes relevant when working with:

```text
Async LLM Calls
Streaming
Concurrent Operations
Async Tools
```

The Python fundamentals were preparation for this stage.

## Development Progression

We will gradually build complexity.

### Stage 1

```text
Prompt
 ↓
Model
```

### Stage 2

```text
Prompt
 ↓
Model
 ↓
Parser
```

### Stage 3

```text
Prompt Template
 ↓
Model
 ↓
Structured Output
```

### Stage 4

```text
Prompt
 ↓
Model
 ↓
Streaming
```

### Stage 5

```text
Async
 ↓
Model
 ↓
Multiple Operations
```

### Stage 6

```text
Retriever
 ↓
Prompt
 ↓
Model
 ↓
Parser
```

Eventually:

```text
Agent
 ↓
Tools
 ↓
Retriever
 ↓
Model
 ↓
Structured Output
```

## Terminology

| Term            | Meaning                                               |
| --------------- | ----------------------------------------------------- |
| LangChain       | Framework for building LLM applications               |
| Chat Model      | Interface for interacting with conversational models  |
| Prompt Template | Reusable prompt structure                             |
| Output Parser   | Converts model output into useful application data    |
| Runnable        | Composable LangChain component                        |
| Chain           | Connected sequence of components                      |
| Retriever       | Finds relevant documents                              |
| Tool            | External capability available to the LLM              |
| Agent           | System that uses tools through a decision-making loop |
| LCEL            | LangChain Expression Language                         |

## Common Mistakes

#### LangChain is an LLM.

Incorrect.

LangChain is a framework.

#### LangChain is required to use OpenAI, Anthropic, Google, etc.

Incorrect.

Provider SDKs can be used directly.

#### LangChain automatically improves model intelligence.

Incorrect.

It provides application-building abstractions.

#### Everything should be built using LangChain.

Incorrect.

Use LangChain when its abstractions provide value.

#### You don't need to understand the underlying model.

Incorrect.

Understanding the underlying concepts helps you debug and design better applications.

#### LangChain and LangGraph are the same.

Incorrect.

They solve different levels of application orchestration.

## Best Practices

### Understand the Underlying LLM

Know what happens with:

```text
Prompt
 ↓
Messages
 ↓
Model
 ↓
Response
```

before abstracting it.

### Start Simple

Start with:

```text
Prompt → Model
```

instead of immediately building:

```text
Agent + RAG + Tools + Memory
```

### Understand Every Abstraction

When you see:

```python
prompt | model | parser
```

you should know what each component represents.

### Debug Individual Components

Don't only inspect the final response.

Inspect:

```text
Prompt
 ↓
Model Input
 ↓
Model Output
 ↓
Parser
```

This makes debugging easier.

### Don't Overuse Abstractions

If a simple provider SDK solves the problem cleanly, LangChain isn't automatically necessary.

## Interview questions

- What is LangChain?
- Why use LangChain instead of directly calling an LLM API?
- Does LangChain improve the intelligence of an LLM?
- Is LangChain an alternative to OpenAI?
