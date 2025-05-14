---
description: "General Python best practices, code style, and linting for Euterpe."
applyTo: "**/*.py"
---

# Python Best Practices for Euterpe

1.  **Code Style:**
    * Follow PEP 8 guidelines.
    * Use **Black** for code formatting. Please format the code accordingly.
    * Use **Ruff** (or Flake8 + isort) for linting and import sorting. Ensure imports are grouped (standard library, third-party, first-party).
2.  **Type Checking:**
    * Use **MyPy** for static type checking. All new code should be type-hinted.
3.  **Logging:**
    * Use the standard `logging` module for any informational, warning, or error messages within the library.
    * Avoid using `print()` statements for logging in library code.
    * Configure a default null handler to prevent "No handler found" warnings if the library user doesn't configure logging.
4.  **Docstrings:**
    * Write clear and concise Google-style docstrings for all modules, classes, functions, and methods.
    * Example:
        ```python
        def my_function(param1: str, param2: int) -> bool:
            """Does something useful.

            Args:
                param1: The first parameter.
                param2: The second parameter.

            Returns:
                True if successful, False otherwise.

            Raises:
                ValueError: If param1 is invalid.
            """
            # ...
        ```
5.  **Testing:**
    * Write unit tests using `pytest`.
    * Aim for good test coverage.
    * Tests should be placed in the `tests/` directory.
6.  **Immutability:**
    * Prefer immutable data structures where possible.
7.  **Readability:**
    * Write code that is easy to read and understand.
    * Use meaningful variable and function names.
    * Break down complex logic into smaller, manageable functions/methods.