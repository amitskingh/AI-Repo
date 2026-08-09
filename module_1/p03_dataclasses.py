from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str


"""
Here every objects shares the same list object in memory, which can lead to unexpected behavior.
"""


@dataclass
class ChatSessionSharedHistory:
    history: list[str] = []  # noqa


"""
Here every object gets its own list object, which is the expected behavior.
"""


@dataclass
class ChatSession:
    history: list[str] = field(default_factory=list)


"""

@dataclass automatically generates the __init__, __repr__, and __eq__ methods for the class, making it easier to create classes that are primarily used to store data.

"""


# Sometimes you want to make a dataclass immutable, meaning that once an instance is created, its attributes cannot be changed. You can achieve this by setting the frozen parameter to True in the @dataclass decorator.
@dataclass(frozen=True)
class DocumentID:
    value: str


# Example usage of the Message class
m1 = Message("user", "Hello")
m2 = Message("user", "Hello")

m3 = Message(
    12, "Hello"
)  # This will raise a type error because the role should be a string.

print(m1)
print(m2)
print(m3)

print(m1 == m2)

# Example usage of Frozen dataclass
doc1 = DocumentID("12345")
# doc1.value = "67890"  # This will raise an error because the dataclass is frozen and its attributes cannot be modified after creation.
