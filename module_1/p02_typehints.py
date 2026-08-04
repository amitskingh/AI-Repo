from typing import Literal, TypedDict


# Basic Type Hints
def count_words(text: str) -> int:
    """Count the number of words in a given text."""
    return len(text.split())


# List type hints
def filter_even_numbers(numbers: list[int]) -> list[int]:
    """Filter even numbers from a list."""
    return [num for num in numbers if num % 2 == 0]


# Optional modern type hints
def find_max(numbers: list[int]) -> int | None:
    """Find the maximum number in a list, return None if the list is empty."""
    if not numbers:
        return None
    return max(numbers)


# Literal type hints example
def set_status(status: Literal["active", "inactive", "pending"]) -> str:
    """Set the status of an entity."""
    return f"Status set to: {status}"


# Typedict type hints example
class User(TypedDict):
    id: int
    name: str
    email: str


print(count_words("Hello world! This is a test."))
print(filter_even_numbers([1, 2, 3, 4, 5, 6]))
print(find_max([10, 20, 30]))
print(set_status("active"))
print(User(id=1, name="Alice", email="alice@example.com"))
