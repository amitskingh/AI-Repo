from collections.abc import Callable
from functools import wraps
from typing import Any


# A simple function that takes a name and returns a greeting message.
def greet(name: str) -> str:
    return f"Hello, {name}!"


# A decorator that logs the greeting message before calling the greet function.
def logged_greet(name: str) -> str:
    # Log the greeting message
    print(f"Logging: Greeting {name}")
    return greet(name)


# Callable type hint format:
# Callable[[arg1_type, arg2_type, ...], return_type]
#
# Examples:
# Callable[[], int]             -> Function with no arguments, returns int
# Callable[[str], str]          -> Function taking one str, returns str
# Callable[[int, float], bool]  -> Function taking int and float, returns bool
# Callable[..., str]            -> Function with any arguments, returns str
def add_logging_decorator(func: Callable[[str], str]) -> Callable[[str], str]:
    """
    A decorator that adds logging to any function that takes a name as an argument.
    """

    def wrapper(name: str) -> str:
        print(f"Logging: Calling {func.__name__} with argument '{name}'")
        return func(name)

    return wrapper


# Shorter version of the decorator using the @ syntax
@add_logging_decorator
def greet_2(name: str) -> str:
    """
    A private function that takes a name and returns a greeting message.
    This function is not intended to be called directly.
    """
    return f"Hello, {name}!"


def retry(max_attempts: int):
    def decorator(function):
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Exception | None = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)
                except Exception as error:  # noqa
                    last_error = error
                    print(f"Attempt {attempt} failed")

            if last_error is not None:
                raise last_error

            raise RuntimeError("Function did not execute")

        return wrapper

    return decorator


@retry(max_attempts=3)
def calculate_total_price(prices: list[float]) -> float:
    """
    Calculate the total price from a list of prices.
    """
    return sum(prices)


def example_1() -> float:
    return calculate_total_price([10.0, 20.0, 30.0])


if __name__ == "__main__":
    print("==================================================")

    # Now call the logged_greet function to see the logging in action.
    message = logged_greet("Alice")
    print(message)

    print("==================================================")
    # Using the add_logging_decorator to add logging to the greet function.
    decorated_greet = add_logging_decorator(greet)
    message = decorated_greet("Bob")
    print(message)

    print("==================================================")
    # Using the add_logging_decorator to add logging to the greet function.
    # Using the add_logging_decorator to add logging to the greet_2 function.
    decorated_greet_2 = add_logging_decorator(greet_2)
    message = decorated_greet_2("Charlie")
    print(message)

    print("==================================================")
    # Using the retry decorator to retry the calculate_total_price function.
    try:
        data = example_1()
        print(f"Total price: {data}")
    except RuntimeError as e:
        # Retry decorator raises RuntimeError if the function did not execute
        print(f"Function failed after retries: {e}")
