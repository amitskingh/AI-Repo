Absolutely. I'll include your **specific confusion and its clarification** in `R09` because that's exactly the kind of thing that will be useful during revision.

````markdown
# R09 – Function Calling & Tool Calling

> **Lesson Goal:** Understand how LLMs interact with external tools/functions, who executes those tools, how structured tool calling works, and how applications safely handle tool requests.

---

# Learning Objectives

After completing this lesson, I should be able to:

- Explain Function Calling / Tool Calling.
- Understand why LLMs need tools.
- Explain who actually executes a tool.
- Understand structured tool calls.
- Differentiate Tool Calling from Agents.
- Understand why type hints and tool schemas matter.
- Understand authentication, authorization, validation, and business logic around tools.
- Understand why an LLM should never be treated as the security boundary.

---

# 1. Why Does Function Calling Exist?

LLMs are primarily designed to generate and process information.

However, real applications need access to external systems such as:

- Databases
- APIs
- Search engines
- Calculators
- Internal services
- File systems
- Business logic

For example:

```text
User:
What's the weather in Delhi?
````

The LLM may not have current weather information.

Instead, it can request:

```text
get_weather(city="Delhi")
```

The application executes the function and returns the result to the LLM.

---

# 2. What Is Function Calling?

Function Calling allows an LLM to produce a structured request asking the application to execute a specific function with specific arguments.

Conceptually:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Application
 ↓
Function
 ↓
Result
 ↓
LLM
 ↓
Final Answer
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

---

# 3. The Most Important Concept

> **The LLM does NOT execute the Python function.**

The LLM only generates a request to call the function.

Your application executes it.

---

# 4. What Does "Application" Mean?

This was an important point of confusion.

When we say **application**, we primarily mean:

> **The code/environment written and controlled by the developer that runs the AI system.**

For example:

```python
@tool
def get_weather(city: str) -> str:
    return weather_api.get(city)
```

The Python function exists in the application's runtime.

LangChain can help expose and orchestrate the function as a tool, but LangChain itself does not magically execute the business operation independently of your application environment.

Conceptually:

```text
User
 ↓
LLM
 ↓
LangChain
 ↓
Tool Call
 ↓
Your Application Code
 ↓
Python Function
 ↓
API / Database
```

### Important distinction

**LangChain helps with:**

* Tool definition
* Tool schemas
* Binding tools to models
* Handling tool-call messages
* Orchestration

**Your application is responsible for:**

* Actual execution
* Business logic
* Authentication
* Authorization
* Validation
* Database/API operations
* Security controls

---

# 5. Simple Python Tool

```python
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is 30°C."
```

The decorator:

```python
@tool
```

allows LangChain to treat the Python function as a tool that can be exposed to the model.

---

# 6. What Does the LLM Actually Receive?

The LLM does not receive executable Python code.

Instead, it receives a structured description/schema of the available tool.

Conceptually:

```json
{
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "parameters": {
        "city": {
            "type": "string"
        }
    }
}
```

The model can then decide:

```text
I should call get_weather.
```

and generate the appropriate structured arguments.

---

# 7. Structured Tool Calling

Without structured tool calling, the model might produce:

```text
I think you should call get_weather for Delhi.
```

The application would then need to parse the text and determine:

```text
Is this a tool call?
Which tool?
What arguments?
```

This is fragile.

With structured tool calling:

```json
{
    "name": "get_weather",
    "arguments": {
        "city": "Delhi"
    }
}
```

the application gets predictable structured information.

### Mental Model

```text
Normal Text
 ↓
Potentially ambiguous
 ↓
Need parsing

Structured Tool Call
 ↓
Defined schema
 ↓
Easier for software to process
```

---

# 8. Function Calling vs Tool Calling

You'll see both terms.

### Function Calling

Originally focused on calling functions.

### Tool Calling

A broader concept that can include:

* Python functions
* APIs
* Search
* Databases
* Other services

Therefore:

```text
Function Calling
      ↓
Specific form of
      ↓
Tool Calling
```

In modern LangChain applications, you'll commonly work with **tools**.

---

# 9. The LLM Doesn't Always Call a Tool

The model can decide whether a tool is necessary.

Example:

```text
User:
What is Python?
```

The LLM can answer directly.

But:

```text
User:
What's the weather in Delhi?
```

The model may request:

```text
get_weather("Delhi")
```

Mental model:

```text
              LLM
               │
       ┌───────┴────────┐
       │                │
 Direct Answer       Tool Call
```

---

# 10. Tool Calling vs Agents

These are related but different.

## Tool Calling

The LLM requests a tool.

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Result
```

---

## Agent

An agent can repeatedly decide what action to take based on previous results.

```text
User
 ↓
LLM
 ↓
Tool A
 ↓
Result
 ↓
LLM
 ↓
Tool B
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

### Key Difference

> **Tool Calling is a capability.**

> **An Agent is a system that uses tools through a decision-making loop.**

---

# 11. Type Hints and Tool Schemas

Consider:

```python
def get_weather(city: str) -> str: ...
```

Type hints help:

### Developers

Understand expected inputs and outputs.

### Frameworks

Generate useful schemas for tools.

Conceptually:

```text
Python Function
 ↓
Type Hints
 ↓
Tool Schema
 ↓
LLM
```

The model can understand:

```text
city → string
```

rather than dealing with an ambiguous function definition.

---

# 12. Why Tool Descriptions Matter

Consider:

```python
@tool
def search_hoa(
    community: str,
    year: int,
) -> str:
    """Search HOA information for a community and year."""
```

The model needs to understand:

```text
Tool:
search_hoa

Parameters:
community → string
year → integer
```

Clear descriptions help the model determine:

* What the tool does
* When to use it
* What parameters are required

---

# 13. Example – Database Tool

Suppose an HOA assistant needs to answer:

> "How many active communities do we have?"

We could provide:

```python
@tool
def get_active_communities() -> int:
    """Return the number of active communities."""
    ...
```

The flow becomes:

```text
User
 ↓
LLM
 ↓
get_active_communities()
 ↓
Application
 ↓
PostgreSQL
 ↓
Result
 ↓
LLM
 ↓
Answer
```

---

# 14. Security – The Most Important Production Concept

The LLM should **never be treated as the security boundary**.

Suppose we have:

```python
delete_community(community_id)
```

The LLM requests:

```text
delete_community(123)
```

Should we immediately execute it?

**No.**

The request must go through application-level security controls.

---

# 15. Safe Tool Execution

A production flow can look like:

```text
User Request
     ↓
LLM
     ↓
Tool Request
     ↓
Authentication
     ↓
Authorization
     ↓
Input Validation
     ↓
Business Logic
     ↓
User Confirmation
     ↓
Risk / Fraud Checks
     ↓
Execute Tool
```

Only after the necessary checks should the operation happen.

---

# 16. Authentication

Authentication answers:

> **Who is the user?**

Example:

```text
Is this user logged in?
```

---

# 17. Authorization

Authorization answers:

> **Is this user allowed to perform this operation?**

Example:

```text
Does this user have permission
to delete community 123?
```

Authentication and authorization are different.

```text
Authentication
    ↓
Who are you?

Authorization
    ↓
What are you allowed to do?
```

---

# 18. Input Validation

Never blindly trust model-generated arguments.

Example:

```json
{
    "amount": 50000
}
```

The application should validate:

* Correct type
* Valid range
* Valid account
* Valid community/user ID
* Required fields

---

# 19. Business Logic

Validation alone isn't enough.

For example:

```text
Transfer ₹50,000
```

The application must check:

```text
Does the account have enough balance?
```

Business rules belong to the application/backend, not the LLM.

---

# 20. User Confirmation

For high-impact actions, confirmation may be required.

Examples:

```text
Delete community
Transfer money
Send email
Cancel subscription
```

Possible flow:

```text
User Request
 ↓
LLM Tool Call
 ↓
Validation
 ↓
Ask User for Confirmation
 ↓
User Confirms
 ↓
Execute
```

Not every tool needs confirmation.

Read-only operations such as:

```text
get_weather()
search_documents()
get_community_details()
```

usually have much lower risk.

---

# 21. Important Security Principle

The LLM can say:

```text
"I want to delete community 123."
```

But the application decides:

```text
Is the user authenticated?
        ↓
Does the user have permission?
        ↓
Is the input valid?
        ↓
Does business logic allow it?
        ↓
Is confirmation required?
        ↓
Execute
```

Therefore:

> **LLM decision ≠ Application authority**

---

# 22. Example – Money Transfer

Suppose the user says:

> Transfer ₹50,000 to John's account.

The LLM generates:

```json
{
    "name": "transfer_money",
    "arguments": {
        "from_account": "user_123",
        "to_account": "john_456",
        "amount": 50000
    }
}
```

The application should NOT immediately execute it.

Instead:

```text
Tool Call
 ↓
Authentication
 ↓
Authorization
 ↓
Input Validation
 ↓
Balance / Business Rules
 ↓
Fraud / Risk Checks
 ↓
User Confirmation
 ↓
Execute Transfer
```

This is the safe architecture.

---

# 23. Tool Categories

A useful production distinction is:

## Read-only tools

Examples:

```text
search_documents()
get_weather()
get_community_details()
get_account_balance()
```

Usually lower risk.

---

## Mutating / Destructive tools

Examples:

```text
delete_community()
transfer_money()
send_email()
cancel_subscription()
```

Higher risk.

These generally require stronger validation, authorization, and potentially confirmation.

---

# 24. Best Practices

### 1. Give Tools Narrow Responsibilities

Prefer:

```python
get_user_orders(user_id)
```

over:

```python
do_anything_in_database(...)
```

---

### 2. Use Strong Typing

```python
def get_weather(city: str) -> str:
```

---

### 3. Write Clear Tool Descriptions

Explain:

* What the tool does
* When to use it
* What its parameters mean

---

### 4. Validate Tool Arguments

Never blindly execute model-generated arguments.

---

### 5. Keep Authorization Outside the LLM

Use application/backend authorization.

---

### 6. Log Tool Calls

For production systems, log useful information such as:

```text
User
Tool
Arguments
Result
Timestamp
Success / Failure
```

Avoid logging sensitive information unnecessarily.

---

### 7. Minimize Tool Permissions

Only give a model the tools it actually needs.

---

# 25. Common Mistakes

### ❌ The LLM executes Python functions.

**Incorrect.**

The application executes them.

---

### ❌ LangChain itself owns the database operation.

**Incorrect.**

LangChain can orchestrate the tool call, but the actual operation occurs in your application/backend environment.

---

### ❌ Tool Calling = Agent.

**Incorrect.**

Tool Calling is a capability.

Agents use tools as part of a decision-making loop.

---

### ❌ Type hints are only for humans.

**Incorrect.**

They also help frameworks construct structured tool schemas.

---

### ❌ The LLM can perform authorization.

**Incorrect.**

Authorization belongs to the application/backend.

---

### ❌ Every tool requires confirmation.

**Incorrect.**

Confirmation depends on the risk and impact of the operation.

---

# Mentor Discussions

## Q: What does "Application" mean?

**Answer:**

The application is the code/runtime controlled by the developer.

LangChain can help orchestrate the tool call, but the application's code and backend execute the actual operation.

---

## Q: Why is structured tool calling better than plain text?

**Answer:**

Plain text can be ambiguous and requires fragile parsing.

Structured tool calls provide predictable tool names and arguments that software can process reliably.

---

## Q: Who executes the function?

**Answer:**

The application's runtime executes the function.

The LLM only requests the function call.

---

## Q: Why are type hints useful?

**Answer:**

They improve developer understanding and help frameworks generate structured schemas describing expected tool inputs and outputs.

---

## Q: Should a delete operation execute immediately after the LLM requests it?

**Answer:**

No.

It should go through the appropriate authentication, authorization, validation, business rules, and potentially user confirmation before execution.

---

# Key Takeaways

* Function Calling allows an LLM to request external functionality.
* Tool Calling is the broader modern concept.
* The LLM requests the tool; the application executes it.
* LangChain helps define and orchestrate tools.
* Structured tool calls are easier and safer for applications to process.
* Type hints help generate useful tool schemas.
* Tool Calling and Agents are different.
* The LLM must not be treated as the security boundary.
* Authentication, authorization, validation, and business logic belong to the application.
* High-risk operations may require user confirmation.

---

# New Terminology

| Term             | Meaning                                                   |
| ---------------- | --------------------------------------------------------- |
| Function Calling | LLM requests execution of a function                      |
| Tool Calling     | Broader mechanism for LLM interaction with tools          |
| Tool             | External capability exposed to an LLM                     |
| Tool Schema      | Structured description of a tool and its parameters       |
| Tool Call        | Structured request generated by the LLM                   |
| Authentication   | Verifying who the user is                                 |
| Authorization    | Verifying what the user is allowed to do                  |
| Business Logic   | Application-specific rules governing an operation         |
| Confirmation     | Explicit approval from the user before a sensitive action |
| Agent            | System that uses tools through a decision-making loop     |

---

# Interview Nuggets

### Q: What is Function Calling?

**Answer:**

Function Calling allows an LLM to generate a structured request for an application to execute a specific function with specified arguments.

---

### Q: Does the LLM execute the function?

**Answer:**

No. The LLM generates the tool request, while the application executes the function.

---

### Q: What is the difference between Tool Calling and Agents?

**Answer:**

Tool Calling allows an LLM to request a tool. An Agent uses tools as part of a loop where it repeatedly decides what action to take based on previous results.

---

### Q: Why is structured tool calling useful?

**Answer:**

It provides predictable structured tool names and arguments, avoiding unreliable parsing of natural-language responses.

---

### Q: Should the LLM perform authorization?

**Answer:**

No. Authorization should be enforced by the application's backend/security layer.

---

# Connections

Previous:

* R01 – What is an LLM?
* R02 – Tokens
* R03 – Context Window
* R04 – Temperature
* R05 – Top-p
* R06 – Prompt Engineering
* R07 – Embeddings
* R08 – Transformers

Next:

* R10 – Structured Output

---

# Summary

Function Calling allows an LLM to request external actions using structured tool calls.

The core architecture is:

```text
User
 ↓
LLM
 ↓
Structured Tool Call
 ↓
Application
 ↓
Authentication / Authorization / Validation
 ↓
Business Logic
 ↓
Tool Execution
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

The most important principle is:

> **The LLM can request an action, but the application decides whether that action is allowed and executes it.**

```
```
