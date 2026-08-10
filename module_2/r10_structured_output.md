# 10 – Structured Output

## The Problem With Normal LLM Output

Suppose we ask an LLM:

```text
Extract the candidate's information.
```

The model might respond:

```text
John Doe has 7 years of experience.
He knows Python, Django and AWS.
He is currently working as a backend developer.
```

A human can understand this.

But an application needs predictable fields such as:

```text
name
experience_years
skills
job_title
```

The application would need to parse arbitrary natural language.

## Why Free-form Output Is Difficult

The same information could be returned in different formats.

#### Response 1

```text
John Doe
7 years
Python, Django, AWS
```

#### Response 2

```text
Candidate: John Doe
Experience: 7 years
Skills: Python, Django, AWS
```

#### Response 3

```json
{
    "name": "John Doe",
    "experience_years": 7,
    "skills": [
        "Python",
        "Django",
        "AWS"
    ]
}
```

The information is similar, but the structure differs.

This makes application-side parsing unreliable.

## What Is Structured Output?

Structured Output means:

> **The LLM returns data following a predefined structure or schema.**

Example:

```json
{
    "name": "John Doe",
    "experience_years": 7,
    "skills": [
        "Python",
        "Django",
        "AWS"
    ]
}
```

The application knows what fields to expect.

## Free-form vs Structured Output

### Free-form

```text
John Doe has 7 years of experience
and knows Python, Django and AWS.
```

The application must interpret the text.

### Structured

```json
{
    "name": "John Doe",
    "experience_years": 7,
    "skills": [
        "Python",
        "Django",
        "AWS"
    ]
}
```

The application can directly access:

```python
data["name"]
data["experience_years"]
data["skills"]
```

## Why Is JSON Popular?

JSON is commonly used because it is:

- Machine-readable
- Human-readable
- Widely supported
- Easy to transmit through APIs
- Easy to convert into application data structures

Example:

```json
{
    "name": "John Doe",
    "age": 30
}
```

## JSON Alone Is Not Enough

Simply asking:

```text
Return JSON.
```

does not necessarily define the exact structure your application expects.

For example, the model could return:

```json
{
    "name": "John Doe",
    "experience_years": "seven"
}
```

But the application expects:

```text
experience_years → integer
```

The model returned:

```text
"seven" → string
```

Therefore, we need more than just JSON.

We need:

```text
Schema
+
Validation
```

## What Is a Schema?

A schema defines the expected structure of the data.

For example:

```text
Candidate
│
├── name → string
├── experience_years → integer
└── skills → list of strings
```

In Python, we can define this using Pydantic.

## Pydantic

Pydantic is a Python library commonly used for defining data models and validating data.

Example:

```python
from pydantic import BaseModel

class Candidate(BaseModel):
    name: str
    experience_years: int
    skills: list[str]
```

This defines the expected structure.

## Creating a Pydantic Object

```python
candidate = Candidate(
    name="John Doe",
    experience_years=7,
    skills=["Python", "Django", "AWS"],
)
```

We can then access:

```python
candidate.name
```

Result:

```text
John Doe
```

And:

```python
candidate.experience_years
```

Result:

```text
7
```

## Validation

Suppose we provide invalid data:

```python
Candidate(
    name="John Doe",
    experience_years="invalid",
    skills=["Python"],
)
```

The schema expects:

```text
experience_years → int
```

Pydantic validates the data and can raise a validation error when the value cannot satisfy the expected type.

This makes Pydantic useful for handling structured LLM output.

## LLM + Pydantic

The general architecture becomes:

```text
User Input
    ↓
LLM
    ↓
Structured Output
    ↓
Pydantic Schema
    ↓
Validation
    ↓
Application
```

Instead of manually parsing arbitrary natural language, the application works with a predefined structure.

## LangChain Structured Output

LangChain provides a convenient mechanism for associating a schema with a chat model.

Example:

```python
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class Candidate(BaseModel):
    name: str
    experience_years: int
    skills: list[str]

model = ChatOpenAI(
    model="gpt-4.1-mini",
)

structured_model = model.with_structured_output(Candidate)
```

Then:

```python
result = structured_model.invoke("Extract candidate information from this resume.")
```

The result can be handled according to the defined schema rather than relying on arbitrary free-form text.

## Conceptual Flow

```text
Resume
   ↓
LLM
   ↓
Structured Output
   ↓
Candidate Schema
   ↓
Validation
   ↓
Candidate Object
```

## Example – HOA Compliance Report

Instead of:

```text
The document appears to have three compliance
issues. The first relates to notice requirements...
```

we can define:

```python
class ComplianceIssue(BaseModel):
    issue: str
    severity: str
    explanation: str

class ComplianceReport(BaseModel):
    summary: str
    issues: list[ComplianceIssue]
```

The resulting structure could be:

```json
{
    "summary": "The document contains three potential issues.",
    "issues": [
        {
            "issue": "Notice requirement",
            "severity": "high",
            "explanation": "..."
        },
        {
            "issue": "Record retention",
            "severity": "medium",
            "explanation": "..."
        }
    ]
}
```

Now another part of the application can consume the data predictably.

## Structured Output vs Tool Calling

These concepts are related but different.

### Structured Output

The LLM returns structured **data**.

```text
LLM
 ↓
Structured Data
```

Example:

```json
{
    "name": "John",
    "age": 30
}
```

### Tool Calling

The LLM requests an **action**.

```text
LLM
 ↓
Tool Call
 ↓
Application
 ↓
Tool
```

Example:

```json
{
    "name": "get_weather",
    "arguments": {
        "city": "Delhi"
    }
}
```

## Core idea
Think:

```text
Structured Output
=
"Give me information in this format."
```

while:

```text
Tool Calling
=
"Request this action with these arguments."
```

## Structured Output vs JSON Mode

These terms are related but should not be treated as identical.

### JSON Mode

Generally means:

> Return valid JSON.

However, the exact fields and types may still require additional schema handling and validation.

### Structured Output

Means:

> Return data according to a defined schema.

Example:

```text
Candidate
├── name: string
├── experience_years: integer
└── skills: list[string]
```

Structured output is therefore more useful when the application requires predictable fields and types.

Provider capabilities differ, so always verify the specific model/API's supported structured-output mechanism.

## Structured output is not truth
This is extremely important.

Suppose the schema requires:

```text
experience_years → integer
```

The LLM returns:

```json
{
    "experience_years": 7
}
```

Pydantic may validate this successfully.

But that does NOT prove:

> The candidate actually has 7 years of experience.

Therefore:

```text
Schema Validation
        ≠
Fact Validation
```

Schema validation checks structure and types.

It does not automatically verify real-world truth.

## Common Mistakes

#### JSON means the information is correct.

No.

JSON only describes a data format.

#### Pydantic guarantees factual accuracy.

No.

Pydantic validates data structure and types.

#### Structured Output and Tool Calling are the same.

No.

Structured Output returns data.

Tool Calling requests an action.

#### "Return JSON" is enough for production.

Not necessarily.

Production systems should use explicit schemas and appropriate validation.

#### Structured Output eliminates all LLM errors.

No.

The model can still:

- Extract incorrect information
- Miss information
- Misinterpret information
- Produce semantically incorrect values

## Best Practices

### Define an Explicit Schema

```python
class Candidate(BaseModel):
    name: str
    experience_years: int
    skills: list[str]
```

### Use Strong Types

Prefer:

```python
experience_years: int
```

when the value is truly numeric.

Avoid unnecessarily representing everything as:

```python
experience_years: str
```

### Validate Output

Use:

```text
LLM
 ↓
Structured Output
 ↓
Validation
 ↓
Application
```

Never blindly trust model output.

### Keep Schemas Focused

Only request fields the application actually needs.

Avoid unnecessarily large schemas.

### Handle Validation Failures

Your application should have a strategy for invalid output.

Possible strategies include:

```text
Invalid Output
     ↓
Retry
Repair
Fallback
Ask Again
Log Error
```

The appropriate strategy depends on the application.

### Don't Confuse Structure With Truth

A valid schema does not mean the information is factually correct.

Use domain-specific validation when factual correctness matters.

## Production Architecture

A robust application may look like:

```text
User
 ↓
Prompt
 ↓
LLM
 ↓
Structured Output
 ↓
Schema Validation
 ↓
Business Validation
 ↓
Application Logic
 ↓
Database / API
```

The same principle we've seen with tool calling applies here:

> **The LLM produces information; the application decides what to trust and what to do with it.**

## Interview questions

- What is Structured Output?
- Why is Structured Output important?
- What is the role of Pydantic?
- Does Pydantic guarantee that an LLM's response is factually correct?
- Difference between Structured Output and Tool Calling?
- Why is "Return JSON" not always sufficient?

## Key takeaways

- Free-form LLM responses are difficult for applications to parse reliably.
- Structured Output provides predictable data structures.
- JSON is a common format for structured data.
- JSON alone does not necessarily define the exact schema.
- Pydantic provides schemas and validation in Python.
- LangChain can connect LLMs with structured schemas.
- Structured Output is different from Tool Calling.
- Schema validation does not guarantee factual correctness.
- Production applications should validate LLM output before using it.

## New terminology

| Term | Meaning |
|---|---|
| Structured Output | LLM response following a predefined structure |
| Schema | Definition of expected fields and data types |
| Pydantic | Python library for data models and validation |
| Validation | Checking whether data satisfies defined requirements |
| JSON | Common machine-readable data format |
| JSON Mode | Model output constrained toward valid JSON |
| Structured Output | Output constrained to a defined schema |

## Connections

Previous:

* **R09 – Function Calling & Tool Calling**

Current:

* **R10 – Structured Output**

Next:

* **Module 3 – LangChain Fundamentals**

## Module completion

With R10, the conceptual lessons of Module 1 are complete:

```text
1.1  What is an LLM
1.2  Tokens
1.3  Context Window
1.4  Temperature
1.5  Top-p
1.6  Prompt Engineering
1.7  Embeddings
1.8  Transformers
1.9  Function / Tool Calling
1.10 Structured Output
```

## Final mental model

```text
                         USER
                           │
                           ▼
                         PROMPT
                           │
                           ▼
                         TOKENS
                           │
                           ▼
                       EMBEDDINGS
                           │
                           ▼
                      TRANSFORMER
                           │
                           ▼
                NEXT TOKEN PROBABILITIES
                           │
                           ▼
                  TEMPERATURE / TOP-P
                           │
                           ▼
                      NEXT TOKEN
                           │
                           ▼
                      GENERATION
                           │
                           ▼
                  STRUCTURED OUTPUT
                           │
                           ▼
                      VALIDATION
                           │
                           ▼
                      APPLICATION
```

When external capabilities are required:

```text
                         LLM
                          │
                 ┌────────┴────────┐
                 │                 │
            Direct Answer      Tool Call
                                   │
                                   ▼
                           Your Application
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                   API             DB           Search
                    │              │              │
                    └──────────────┼──────────────┘
                                   ▼
                                  LLM
                                   │
                                   ▼
                                Answer
```

## Final principle

> **The LLM generates information and decisions, while the application provides structure, validation, security, authorization, and execution.**

This principle will continue to appear throughout LangChain, RAG, Agents, and LangGraph.
