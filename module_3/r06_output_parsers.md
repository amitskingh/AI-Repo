# 6 – Output Parsers & Structured Output

## The Problem

LLMs naturally produce human-readable responses.

For example:

```text
The user's name is John, he is 32 years old,
and his email is john@example.com.
```

A human can easily understand this.

But an application would often prefer:

```json
{
    "name": "John",
    "age": 32,
    "email": "john@example.com"
}
```

Now the application can work with predictable fields:

```python
result["name"]
result["age"]
result["email"]
```

Therefore:

```text
Human-readable output
        ↓
       LLM
        ↓
Application-readable output
```

## Why Structured Output Matters

Applications often need predictable data for:

* APIs
* Databases
* UI rendering
* Business logic
* Validation
* Automation
* Tool calling
* Workflow execution

Natural language:

```text
John is 32 years old.
```

Structured data:

```json
{
    "name": "John",
    "age": 32
}
```

The second representation is easier for application code to consume.

## Where Output Parsing Comes In

Our previous chain was:

```text
Prompt
   ↓
Chat Model
   ↓
AIMessage
```

We can add an output-processing step:

```text
Prompt
   ↓
Chat Model
   ↓
AIMessage
   ↓
Output Parser
   ↓
Application Data
```

Conceptually:

```text
Input
 ↓
Prompt
 ↓
LLM
 ↓
AIMessage
 ↓
Parser
 ↓
Application-friendly result
```

## What Is an Output Parser?

An Output Parser is a component that processes model output and transforms it into a representation that the application can use.

Conceptually:

```text
LLM Output
    ↓
Output Parser
    ↓
Application Data
```

Depending on the parser, the result may be:

```text
String
JSON-like data
List
Pydantic object
Other structured representation
```

## Why Not Just Tell the Model to Return JSON?

We can write:

```text
Return the result as JSON.
```

The model may return:

```json
{
    "name": "John",
    "age": 32
}
```

But it might also return:

```text
Sure! Here is the JSON:

{
    "name": "John",
    "age": 32
}
```

Or:

```json
{
    "full_name": "John",
    "age": "32"
}
```

Or malformed JSON.

Therefore:

> Asking the model to return JSON does not by itself guarantee reliable application-level structure.

Structured-output mechanisms and validation can improve reliability.

## `StrOutputParser`

One of the simplest parsers is:

```python
from langchain_core.output_parsers import StrOutputParser
```

It is useful when the application wants the model response as a plain string.

Example:

```python
parser = StrOutputParser()
```

Flow:

```text
AIMessage
    ↓
StrOutputParser
    ↓
String
```

## Why Use `StrOutputParser`?

A Chat Model generally returns an `AIMessage`.

For example:

```python
response = model.invoke(
    "Explain RAG."
)
```

Conceptually:

```text
AIMessage
```

If the application only wants the generated text:

```text
"RAG is..."
```

then:

```text
AIMessage
    ↓
StrOutputParser
    ↓
String
```

is useful.

## Chain With `StrOutputParser`

We can compose:

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

chain = prompt | model | parser
```

Then:

```python
result = chain.invoke(
    {
        "topic": "RAG"
    }
)
```

The final result is a string.

Architecture:

```text
Input
 ↓
Prompt
 ↓
Chat Model
 ↓
AIMessage
 ↓
StrOutputParser
 ↓
String
```

## Why Is This Useful?

Without a parser:

```python
response = model.invoke(...)
print(response.content)
```

With a parser:

```python
chain = prompt | model | StrOutputParser()

result = chain.invoke(...)
```

Now the chain itself describes the complete transformation:

```text
Input
 ↓
Prompt
 ↓
Model
 ↓
String
```

This is especially useful when composing larger workflows.

## Structured Output

Suppose we want:

```json
{
    "name": "John",
    "age": 32,
    "email": "john@example.com"
}
```

Instead of arbitrary natural language.

We need to define the expected structure.

Conceptually:

```text
Person
├── name: string
├── age: integer
└── email: string
```

This definition is called a schema.

## What Is a Schema?

A schema defines the expected structure of data.

For example:

```text
Person
{
    name: string
    age: integer
    email: string
}
```

The schema tells us:

```text
name  → string
age   → integer
email → string
```

This makes the expected output explicit.

## Pydantic

In Python, Pydantic is commonly used to define and validate structured data.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str
```

Now we have:

```text
User
├── name  → str
├── age   → int
└── email → str
```

## Why Validation Matters

Suppose the model produces:

```json
{
    "name": "John",
    "age": "thirty-two",
    "email": "john@example.com"
}
```

But our schema expects:

```text
age → integer
```

Validation can detect that the output doesn't satisfy the expected structure.

Therefore:

```text
LLM Output
    ↓
Validation
    ↓
Valid / Invalid
```

## Treat LLM output as untrusted
This is an important production principle.

Even if the model produces:

```json
{
    "age": 32
}
```

the application should not blindly assume:

> The model generated it, therefore it must be valid.

Instead:

```text
LLM
 ↓
Structured Output
 ↓
Validation
 ↓
Business Logic
```

Treat model-generated information as untrusted application input.

## `model.with_structured_output()`

Modern LangChain model integrations can expose structured-output capabilities.

Conceptually:

```python
class Person(BaseModel):
    name: str
    age: int

structured_model = model.with_structured_output(Person)
```

Then:

```python
result = structured_model.invoke(
    "John is 32 years old."
)
```

The result can conceptually be:

```text
Person(
    name="John",
    age=32
)
```

The exact behavior depends on the model/provider integration.

## Why `with_structured_output()` Is Useful

Instead of:

```text
Prompt
 ↓
LLM
 ↓
Raw Text
 ↓
Parse Manually
 ↓
Validate
```

we can use a structured-output capability:

```text
Schema
 ↓
Chat Model
 ↓
Structured Result
```

When supported by the model/provider, this can provide stronger guarantees than simply asking the model to "return JSON."

## Output Parser vs Structured Output

These concepts are related but not identical.

### Output Parser

Processes model output:

```text
Model Output
    ↓
Parser
    ↓
Desired Representation
```

Example:

```text
AIMessage
    ↓
StrOutputParser
    ↓
String
```

### Structured Output

Defines the structure expected from the model:

```text
Schema
    ↓
Model
    ↓
Structured Result
```

Example:

```text
Person Schema
    ↓
Chat Model
    ↓
Person Object
```

Therefore:

```text
Output Parser
    ≠
Structured Output
```

They can solve related problems using different approaches.

## Three approaches
You do NOT need to memorize every parser.

For now, remember these three categories.

### I only need plain text

```python
StrOutputParser()
```

Flow:

```text
LLM
 ↓
String
```

### I need structured data and the model supports it

```python
model.with_structured_output(MySchema)
```

Flow:

```text
LLM
 ↓
Structured Object
```

### I specifically need to parse/transform raw model output

Use an appropriate Output Parser.

Flow:

```text
LLM
 ↓
Output Parser
 ↓
Desired Representation
```

## Other Output Parsers

`StrOutputParser` is not the only parser.

LangChain provides other specialized output parsers, including parsers for concepts such as:

```text
String
JSON
Pydantic objects
Lists
Structured key/value output
XML
Other structured formats
```

Examples include:

```python
StrOutputParser
JsonOutputParser
PydanticOutputParser
```

The exact available parsers and recommended usage can vary with the LangChain version and integration.

The goal is not to memorize every parser.

Understand the category:

```text
Model Output
    ↓
Parser
    ↓
Desired Application Representation
```

## `JsonOutputParser`

A JSON-oriented parser can process JSON-style model output.

Conceptually:

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

chain = prompt | model | parser
```

Flow:

```text
Model
 ↓
JSON Parser
 ↓
Python dict-like result
```

Example:

```json
{
    "name": "John",
    "age": 32
}
```

However, if the model integration supports:

```python
model.with_structured_output(MySchema)
```

that may be a more appropriate modern approach for schema-based structured output.

## `PydanticOutputParser`

LangChain also provides a Pydantic-based parser.

Conceptually:

```python
from langchain_core.output_parsers import PydanticOutputParser
```

Flow:

```text
Model
 ↓
PydanticOutputParser
 ↓
Pydantic Object
```

This is useful when explicitly managing parsing and validation through a Pydantic schema.

Do not confuse this with:

```python
model.with_structured_output(MyModel)
```

They are different mechanisms.

## Structured Output vs Tool Calling

These concepts are related but should not be treated as identical.

### Structured Output

The model produces structured application data.

Example:

```json
{
    "name": "John",
    "age": 32
}
```

Meaning:

> "Here is the information."

### Tool Calling

The model produces a structured request to execute a capability.

Example:

```json
{
    "tool": "get_weather",
    "arguments": {
        "city": "Delhi"
    }
}
```

Meaning:

> "Please execute this capability with these arguments."

## Core idea
```text
                 LLM
                  │
         ┌────────┴────────┐
         │                 │
         ▼                 ▼
 Structured Output     Tool Calling
         │                 │
         ▼                 ▼
 Application Data      Tool Request
                           │
                           ▼
                      Application
                           │
                           ▼
                         Tool
```

Structured Output:

```text
Data for the application
```

Tool Calling:

```text
Request for the application to execute a capability
```

## Schema Validation vs Business Validation

This distinction is extremely important.

### Schema Validation

Checks:

```text
age → integer
name → string
email → string
```

It answers:

> Does this data have the expected structure and types?

### Business Validation

Checks application rules:

```text
age >= 18
community belongs to user
user has sufficient balance
email belongs to allowed domain
```

It answers:

> Is this data allowed according to the application's rules?

Therefore:

```text
Schema Validation
       ≠
Business Validation
```

## Example – HOA Application

Suppose the model extracts:

```json
{
    "community": "Sunset Villas",
    "issue": "Broken gate",
    "priority": "high"
}
```

Schema validation checks:

```text
community → string
issue → string
priority → allowed type/value
```

But business logic must check:

```text
Does the community exist?
Does the user belong to the community?
Is the user authorized to create this request?
Is high priority allowed?
```

Therefore:

```text
Structured Output
       ↓
Schema Validation
       ↓
Authorization
       ↓
Business Logic
       ↓
Action
```

## Structured Does Not Mean Correct

This is a critical principle.

Suppose the model returns:

```json
{
    "age": -50
}
```

This may satisfy:

```text
age → integer
```

but it may violate:

```text
age >= 0
```

Therefore:

```text
Structured
    ≠
Correct
```

## Structured Does Not Mean Safe

Suppose the model returns:

```json
{
    "community_id": 123,
    "action": "delete"
}
```

This is perfectly structured.

But it doesn't mean the application should execute it.

The application still needs:

```text
Authentication
Authorization
Input Validation
Business Logic
Confirmation
```

Therefore:

```text
Structured
    ≠
Safe
```

## Structured Does Not Mean Authorized

A model can generate:

```json
{
    "community_id": 123,
    "action": "delete"
}
```

But only the application should determine:

```text
Is the user authorized?
```

Never:

```text
LLM says delete
    ↓
Delete immediately
```

Instead:

```text
LLM
 ↓
Structured Tool Request
 ↓
Application
 ↓
Authentication
 ↓
Authorization
 ↓
Validation
 ↓
Business Rules
 ↓
Confirmation
 ↓
Tool Execution
```

## Output Parser in a Chain

Our LangChain architecture has now evolved.

Previously:

```text
Prompt
 ↓
Chat Model
 ↓
AIMessage
```

Now:

```text
Prompt
 ↓
Chat Model
 ↓
AIMessage
 ↓
Output Parser
 ↓
Application Data
```

In code:

```python
chain = prompt | model | parser
```

This is one of the most important LangChain composition patterns.

## Plain Text Example

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful teacher."
        ),
        (
            "human",
            "Explain {topic}."
        ),
    ]
)

model = ChatOpenAI(
    model="gpt-4.1-mini"
)

parser = StrOutputParser()

chain = prompt | model | parser

result = chain.invoke(
    {
        "topic": "RAG"
    }
)

print(result)
```

Architecture:

```text
Input
 ↓
ChatPromptTemplate
 ↓
Chat Model
 ↓
AIMessage
 ↓
StrOutputParser
 ↓
String
```

## Structured Data Example

Define a schema:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

Then:

```python
structured_model = model.with_structured_output(Person)
```

Conceptually:

```text
Input
 ↓
Structured Chat Model
 ↓
Person
 ├── name
 └── age
```

The exact structured-output behavior depends on the model/provider integration.

## Why Not Always Use an Output Parser?

If all you need is:

```python
response.content
```

then you don't necessarily need a parser.

For example:

```python
response = model.invoke(
    "Explain RAG."
)

print(response.content)
```

is perfectly valid.

Parsers become particularly useful when:

* You want a standardized chain output.
* You need a specific representation.
* You need structured application data.
* You want parsing/validation as part of the workflow.

## Why Not Always Use `with_structured_output()`?

Because sometimes you simply need:

```text
plain text
```

In that case:

```python
StrOutputParser()
```

may be enough.

Or you may specifically need a parser to transform existing model output.

Use the mechanism appropriate to the required result.

## Common Mistakes

#### `StrOutputParser` is the only parser.

Incorrect.

Other parsers include JSON/Pydantic-oriented parsers and other specialized options.

#### `with_structured_output()` is the only way to get structured data.

Incorrect.

There are parser-based approaches as well.

#### Asking the LLM for JSON guarantees valid JSON.

Incorrect.

#### Structured output guarantees correctness.

Incorrect.

It improves structural predictability, not business correctness.

#### Pydantic makes the LLM trustworthy.

Incorrect.

Pydantic validates data against a schema.

#### Structured output replaces authorization.

Incorrect.

Application security is still required.

#### Tool Calling and Structured Output are identical.

Incorrect.

Tool Calling represents a request to execute a capability.

Structured Output represents structured application data.

#### `ToolMessage` is an Output Parser.

Incorrect.

`ToolMessage` is a message containing a tool execution result.

## Best Practices

### Define Explicit Schemas

For structured data:

```python
class Person(BaseModel):
    name: str
    age: int
```

### Validate Model Output

Treat model-generated output as untrusted input.

### Separate Schema Validation From Business Logic

Use:

```text
Schema
 ↓
Type/Structure Validation
 ↓
Business Rules
```

### Prefer Provider-Supported Structured Output When Appropriate

When the model/provider supports reliable structured output, it can be preferable to asking the model to return arbitrary JSON and parsing it afterward.

### Use Parsers When You Actually Need Them

Don't add parsers simply because LangChain provides them.

Choose based on the desired output.

### Don't Use Structured Output as a Security Mechanism

Structured output improves predictability.

It does not replace:

```text
Authentication
Authorization
Business Rules
Confirmation
```

## Interview questions

- What is an Output Parser?
- What is `StrOutputParser`?
- What is structured output?
- Why is structured output useful?
- Does structured output guarantee valid business data?
- Does structured output replace security?
- What is `PydanticOutputParser`?
- What is `JsonOutputParser`?

## Quick revision

| Concept                    | Meaning                                     |
| -------------------------- | ------------------------------------------- |
| Output Parser              | Transforms model output                     |
| `StrOutputParser`          | Converts output to string                   |
| `JsonOutputParser`         | Parses JSON-style output                    |
| `PydanticOutputParser`     | Parses/validates using Pydantic             |
| Structured Output          | Output following a defined schema           |
| `with_structured_output()` | Model interface for structured results      |
| Schema                     | Definition of expected fields/types         |
| Pydantic                   | Python library for data modeling/validation |
| Schema Validation          | Checks structure/types                      |
| Business Validation        | Checks application rules                    |
| Tool Calling               | Structured request to execute a capability  |

## Security model

Structured output does not change the security architecture.

For example:

```text
LLM
 ↓
{
    "community_id": 123,
    "action": "delete"
}
 ↓
Authentication
 ↓
Authorization
 ↓
Input Validation
 ↓
Business Logic
 ↓
Confirmation
 ↓
Tool Execution
```

Never:

```text
LLM
 ↓
Delete Community
```

## Final mental model

The overall LangChain flow is now:

```text
                    USER INPUT
                         │
                         ▼
                 Prompt Template
                         │
                         ▼
                    Chat Model
                         │
                         ▼
                      AIMessage
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
          Output Parser     Structured Output
                │                 │
                └────────┬────────┘
                         ▼
                  Application Data
                         │
                         ▼
                   Validation
                         │
                         ▼
                  Business Logic
```

Remember:

```text
Structured
    ≠
Correct

Structured
    ≠
Safe

Structured
    ≠
Authorized
```

## Key takeaways

* LLMs naturally generate human-readable responses.
* Applications often need predictable data.
* Output Parsers transform model output into useful representations.
* `StrOutputParser` is useful when plain text is required.
* `JsonOutputParser` and `PydanticOutputParser` are examples of specialized parsers.
* `model.with_structured_output()` is a modern approach for schema-based structured output when supported.
* Output Parsing and Structured Output are related but different concepts.
* Asking the model to "return JSON" does not guarantee reliable JSON.
* Pydantic can define and validate structured data.
* Schema validation checks structure and types.
* Business validation checks application-specific rules.
* Structured output does not guarantee correctness.
* Structured output does not guarantee safety.
* Structured output does not provide authorization.
* Tool Calling and Structured Output are related but have different purposes.
* LangChain allows output processing to be composed into chains.

## One-line summary

> **Output parsing and structured output turn probabilistic model responses into predictable application-friendly data, while validation and business rules remain the application's responsibility.**

## Connections

Previous:

* **R05 – Prompt Templates & Basic Chains**

Current:

* **R06 – Output Parsers & Structured Output**

Next:

* **R07 – Runnables & LCEL**

## Final mental model to memorize

```text
Prompt
   ↓
Chat Model
   ↓
AIMessage
   ↓
┌───────────────────────────┐
│                           │
│ Plain Text                │
│   ↓                       │
│ StrOutputParser           │
│                           │
│ Structured Data           │
│   ↓                       │
│ with_structured_output()  │
│                           │
│ Raw Output Transformation │
│   ↓                       │
│ Appropriate Parser        │
│                           │
└───────────────────────────┘
   ↓
Application Data
   ↓
Validation
   ↓
Business Logic
```

The three things to remember for now:

```text
StrOutputParser
    ↓
Plain text

with_structured_output()
    ↓
Structured data

Tool Calling
    ↓
Structured action request
```

