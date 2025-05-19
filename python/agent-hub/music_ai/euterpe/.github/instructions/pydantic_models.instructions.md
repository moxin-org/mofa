---
description: "Guidelines for creating Pydantic models in the Euterpe project."
applyTo: "**/models.py" # Apply specifically when editing models.py
---

# Pydantic Model Creation Guidelines

When creating or modifying Pydantic models for the `euterpe` project:

1.  **Base Class:** All models MUST inherit from `pydantic.BaseModel`.
2.  **Type Hinting:** All fields MUST have explicit type hints (e.g., `str`, `int`, `List[str]`, `Optional[HttpUrl]`). Use `typing` module imports as needed.
3.  **Field Validation:** Use Pydantic `Field` for validation, default values, or environment variable loading where appropriate (e.g., `Field(default_factory=lambda: os.environ.get("API_KEY"))`).
4.  **Optional Fields:** Clearly distinguish between required and optional fields using `Optional[...]` and provide sensible defaults if a field is optional but typically needed.
5.  **Readability:** Organize models logically. Use nested models for complex data structures.
6.  **Snake Case:** Field names should be `snake_case`.
7.  **Immutability:** Consider making models immutable (`class Config: frozen = True`) if their state should not change after creation, especially for configuration objects.
8.  **API Keys:** API keys in config models should be `Optional[str]` and default to loading from environment variables.

**Example Snippet (for EuterpeConfig):**
```python
from pydantic import BaseModel, Field, HttpUrl, DirectoryPath
from typing import Optional
import os

class EuterpeConfig(BaseModel):
    beatoven_api_key: Optional[str] = Field(default_factory=lambda: os.environ.get("BEATOVEN_API_KEY"))
    kling_api_key: Optional[str] = Field(default_factory=lambda: os.environ.get("KLING_API_KEY"))
    kling_base_url: Optional[HttpUrl] = Field(default_factory=lambda: os.environ.get("KLING_BASE_URL"))
    # ... other config fields