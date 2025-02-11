from typing import Annotated


# Define simple calculator functions
def add_numbers(
    a: Annotated[float, "First number"], b: Annotated[float, "Second number"]
) -> str:
    """Add a and b.

    Args:
        a: first number
        b: second number
    """
    return f"The sum of {a} and {b} is {a + b}."


def multiply_numbers(
    a: Annotated[float, "First number"], b: Annotated[float, "Second number"]
) -> str:
    """Multiply a and b.

    Args:
        a: first number
        b: second number
    """
    return f"The product of {a} and {b} is {a * b}."


def divide_number(
    a: Annotated[float, "First number"], b: Annotated[float, "Second number"]
) -> str:
    """Divide a and b.

    Args:
        a: first number
        b: second number
    """
    return f"The division of {a} by {b} is {a / b}."
