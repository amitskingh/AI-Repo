from pydantic import BaseModel, Field
from dataclasses import dataclass


@dataclass
class Document:
    page_content: str
    metadata: dict = Field(default_factory=dict)


document = Document(
    page_content="The maximum fine is $1,000.",
    metadata={
        "community_id": 101,
        "document_id": "fine_policy",
        "version": "2026",
        "effective_date": "2026-01-01",
        "page": 4,
    },
)


document = Document(
    page_content="The maximum fine is $1,000.",
    metadata={
        "community_id": 101,
        "document_id": "fine_policy",
        "version": "2025",
        "effective_date": "2025-01-01",
        "page": 4,
    },
)

print(document.page_content)
print(document.metadata)
