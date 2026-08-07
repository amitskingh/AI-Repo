# 8 – Virtual Environments & Package Management

Two projects often need different package versions (e.g. LangChain 0.1 + Pydantic 1 vs LangChain 1.x + Pydantic 2). Sharing one global Python install causes **dependency conflicts**. A virtual environment gives each project its own isolated interpreter and packages.

## Create and activate

```bash
python -m venv .venv
```

```bash
# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

The prompt shows `(.venv)`. Installs now go into `.venv/`, not global site-packages.

```bash
pip install langchain
pip list
```

## Pin and share dependencies

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

Example:

```text
langchain==1.0.0
langgraph==0.6.2
openai==1.95.0
pydantic==2.11.0
```

Pinning versions keeps installs reproducible across machines and over time. Modern projects may use `pyproject.toml` for metadata and dependencies; you will see both formats.

## Best practices

- One virtual environment per project
- Activate before installing
- Commit `requirements.txt` or `pyproject.toml` — never commit `.venv/`
- Pin versions when you care about stability

## Common mistakes

- Installing with `pip` while the venv is inactive (packages land globally)
- Creating `.venv` but forgetting to activate it
- Committing `.venv/` to Git — add it to `.gitignore`

## AI / LangChain connection

Install framework packages inside a venv so projects stay isolated:

```bash
pip install langchain langgraph openai
```

## Interview questions

- What is a virtual environment? Why use one?
- Global Python vs a venv? What is `requirements.txt`?
- Why do dependency conflicts happen? `requirements.txt` vs `pyproject.toml`? Why pin versions?

## Summary

Virtual environments isolate dependencies. Together with a pinned dependency file, they are the baseline for every professional Python—and AI—project.
