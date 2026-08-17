# Module 3 – LangChain Fundamentals

Build LLM apps with LangChain: chat models, messages, prompt templates, chains, and structured output—without treating the framework as magic.

This module applies the ideas from Module 2 (tokens, context, temperature, tools, structured output) inside LangChain’s composition style.

## Learning objectives

By the end of this module you should be able to:

- Explain what LangChain is and is not (framework vs model)
- Set up a project, API keys, and a first `ChatOpenAI` call
- Work with chat models and message roles (`System`, `Human`, `AI`, `Tool`)
- Build reusable prompts with `PromptTemplate` / `ChatPromptTemplate`
- Compose a basic chain with `|` and `invoke()`
- Parse plain text and structured output (`StrOutputParser`, schemas, Pydantic)

## Prerequisites

- [Module 1 – Python Essentials](../module_1/README.md)
- [Module 2 – LLM Fundamentals](../module_2/README.md)
- Basic familiarity with virtual environments and `.env` files

## Roadmap

```
LangChain overview → Installation & setup → Chat Models → Messages
  → Prompt Templates & Chains → Output Parsers & Structured Output
  → Runnables & LCEL → RAG Fundamentals → Practical RAG Pipeline
  → Retrieval Quality & Advanced Retrieval
  → RAG Evaluation & Production Considerations
```

## Contents

| Note | Topic | Practice |
|------|--------|----------|
| [r01_what_is_langchain.md](r01_what_is_langchain.md) | What is LangChain? | — |
| [r02_installation_setup.md](r02_installation_setup.md) | Installation & project setup | [p01.py](p01.py) |
| [r03_chat_models.md](r03_chat_models.md) | Chat models | [p02.py](p02.py) |
| [r04_messages.md](r04_messages.md) | Messages (System, Human, AI, Tool) | [p02.py](p02.py) |
| [r05_prompt_templates.md](r05_prompt_templates.md) | Prompt templates & basic chains | [p03.py](p03.py), [p04.py](p04.py) |
| [r06_output_parsers.md](r06_output_parsers.md) | Output parsers & structured output | [p05_str_output_parser.py](p05_str_output_parser.py), [p06_structured_output.py](p06_structured_output.py), [p07_pydantic_output_parser.py](p07_pydantic_output_parser.py) |
| [r07_runnables_lcel.md](r07_runnables_lcel.md) | Runnables & LCEL | [p08_runnable_lamda.py](p08_runnable_lamda.py), [p09_runnable_passthrough.py](p09_runnable_passthrough.py), [p10_runnable_parallel.py](p10_runnable_parallel.py), [p11_runnable_sequence.py](p11_runnable_sequence.py), [p12_runnable_branch.py](p12_runnable_branch.py), [p13_runnable_passthrough_paralled.py](p13_runnable_passthrough_paralled.py) |
| [r08_rag_fundamentals.md](r08_rag_fundamentals.md) | RAG fundamentals | — |
| [r09_practical_rag_pipeline.md](r09_practical_rag_pipeline.md) | Practical RAG pipeline | [p14_rag_mini_example.py](p14_rag_mini_example.py) |
| [r10_retrieval_quality.md](r10_retrieval_quality.md) | Retrieval quality & advanced retrieval | — |
| [r11_rag_evaluation.md](r11_rag_evaluation.md) | RAG evaluation & production considerations | — |

## How to use

1. Read each note in order.
2. Run the matching practice file(s) and experiment.
3. Use interview questions, key takeaways, and quick revision sections for self-check.
