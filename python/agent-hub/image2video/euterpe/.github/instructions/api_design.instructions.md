---

**File: `.vscode-ai/instructions/api_design.instructions.md`**
```markdown
---
description: "Guidelines for designing the public API of the Euterpe library."
applyTo: "**/api.py" # Apply specifically when editing api.py
---

# Euterpe API Design Principles

When working on `euterpe/api.py` and defining the public interface:

1.  **Main Entry Point:** The primary function will be `generate_video`.
2.  **Input Structure:** `generate_video` MUST accept a single Pydantic model (`VideoGenerationRequest`) as its primary input for all user-configurable parameters.
3.  **Configuration:**
    * It should accept an optional `EuterpeConfig` Pydantic model.
    * If `EuterpeConfig` is not provided, the system should attempt to load a default configuration (e.g., from environment variables or a default config file, managed by `config_loader.py` or within the `EuterpeWorkflow` class).
4.  **Output Structure:** `generate_video` MUST return a Pydantic model (`VideoGenerationResult`) containing:
    * `success: bool`
    * `video_filepath: Optional[FilePath]`
    * `message: str`
    * `error_details: Optional[str]`
    * Other relevant output paths (e.g., `music_filepath`, `image_filepaths`).
5.  **Simplicity:** The API should be as simple as possible for the common use case. Advanced features can be exposed via optional parameters within the request model.
6.  **Error Handling:** Catch exceptions from the underlying workflow and translate them into a meaningful `VideoGenerationResult` with `success=False`.
7.  **No Side Effects (beyond file creation):** The API function itself should be stateless. State related to a generation job is managed by the workflow instance.
8.  **Exports:** Clearly define what is exported from the `euterpe` package in `euterpe/__init__.py` (e.g., `generate_video`, core Pydantic models, `__version__`).