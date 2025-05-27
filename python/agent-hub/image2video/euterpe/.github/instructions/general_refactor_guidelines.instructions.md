---
description: "General guidelines for refactoring the Euterpe project."
applyTo: "**/*.py" # Apply to all Python files involved in refactoring
---

# Euterpe Project Refactoring: General Guidelines

You are assisting in refactoring the `euterpe` Python project into a modern, installable library.

**Key Objectives:**
1.  **Standard Package Structure:** Adhere to the proposed structure (main package `euterpe/`, submodules like `generators/`, `processors/`, `models.py`, `api.py`).
2.  **Simplified API:** Create a primary API function `generate_video` that accepts a Pydantic model for input and returns a Pydantic model.
3.  **Pydantic for Data Structures:** All data transfer objects (DTOs), configurations, and API request/response bodies MUST use Pydantic models.
4.  **Configuration Management:** API keys and settings should be managed via an `EuterpeConfig` Pydantic model, loadable from environment variables or direct instantiation.
5.  **Modularity:** Break down large files/functions into smaller, focused modules and classes.
6.  **Clear Imports:** Use absolute imports `from euterpe.module import ...` for intra-package imports. Relative imports `from .module import ...` are acceptable within the same sub-package.
7.  **Type Hinting:** All functions and methods MUST have type hints.
8.  **Docstrings:** All public modules, classes, functions, and methods MUST have Google-style docstrings.
9.  **Error Handling:** Implement robust error handling. Use custom exceptions where appropriate. The main API should return a result object indicating success/failure and error details.
10. **Dependency Management:** `pyproject.toml` will be the source of truth for dependencies. `BeatovenDemo` and `KlingDemo` should be treated as installable dependencies.

**Reference:**
* The overall refactoring plan is detailed in `Migration.md`. (You'd put my previous detailed response here or link to it if it's a file in the repo).
* Refer to the proposed directory structure:
    ```
    euterpe_project_root/
    ├── euterpe/
    │   ├── __init__.py
    │   ├── api.py
    │   ├── models.py
    │   ├── main_workflow.py
    │   ├── config_loader.py
    │   ├── enhancers/
    │   ├── processors/
    │   ├── generators/
    │   └── utils/
    ├── lib/
    ├── tests/
    ├── examples/
    ├── pyproject.toml
    └── README.md
    ```