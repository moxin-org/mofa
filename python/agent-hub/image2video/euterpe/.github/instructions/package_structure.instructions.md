---
description: "Guidelines for the Euterpe Python package structure and module organization."
applyTo: "**/*.py" # Apply broadly as it relates to all new/moved Python files
---

# Euterpe Python Package Structure Guidelines

The `euterpe` project is being refactored into an installable Python package named `euterpe-creator`. The source code for the package itself will reside in a directory named `euterpe/`.

**Target Directory Structure:**

euterpe_project_root/
├── euterpe/                       # The main Python package
│   ├── init.py                # Exports public API (generate_video, models, version)
│   ├── api.py                     # Contains generate_video() and related public functions
│   ├── models.py                  # Pydantic models (VideoGenerationRequest, EuterpeConfig, etc.)
│   ├── main_workflow.py           # Core orchestration logic (class EuterpeWorkflow)
│   ├── config_loader.py           # Logic for loading EuterpeConfig
│   │
│   ├── enhancers/                 # Sub-package for text enhancement
│   │   ├── init.py
│   │   └── dify_client.py         # (Refactored from src/dify_enhancer.py)
│   │
│   ├── processors/                # Sub-package for data processing
│   │   ├── init.py
│   │   └── keyframe_rules.py      # (Refactored from src/keyframe_processor.py)
│   │
│   ├── generators/                # Sub-package for generation tasks
│   │   ├── init.py
│   │   ├── image_module.py        # Interface to KlingDemo (from src/image_generator.py)
│   │   ├── music_module.py        # Interface to BeatovenDemo (from src/music_generator.py)
│   │   └── video_assembler.py     # Assembles video (from src/video_generator.py)
│   │
│   └── utils/                     # Optional: for common utility functions
│       ├── init.py
│       └── file_utils.py
│
├── lib/                           # Contains BeatovenDemo and KlingDemo
│   ├── BeatovenDemo/
│   └── KlingDemo/
│
├── tests/                         # Pytest tests
│   ├── init.py
│   ├── test_api.py
│   └── test_workflow.py
│
├── examples/                      # Example usage scripts
│   ├── simple_video_generation.py
│   └── sample_request.json
│
├── pyproject.toml                 # Packaging and dependency definition
├── README.md
└── LICENSE
└── .gitignore


**Key Points for Module Placement:**

1.  **`euterpe/` is the Package Root:** All core library code goes here or in its subdirectories.
2.  **`euterpe/__init__.py`:**
    * Define `__version__`.
    * Export the main public API elements (e.g., `from .api import generate_video`, `from .models import VideoGenerationRequest`). Use `__all__`.
3.  **`euterpe/api.py`:** Location for the main `generate_video` function and any other direct, high-level user-facing functions.
4.  **`euterpe/models.py`:** All Pydantic models used for API requests, responses, and internal configuration.
5.  **`euterpe/main_workflow.py`:** The `EuterpeWorkflow` class that orchestrates the video generation process.
6.  **`euterpe/config_loader.py`:** Handles loading of `EuterpeConfig`, potentially from environment variables, files, or direct instantiation defaults.
7.  **Sub-packages (`enhancers/`, `processors/`, `generators/`):**
    * Each should have an `__init__.py`.
    * Group related functionality. For example, all code interfacing with image generation services goes into `generators/image_module.py`.
8.  **Original `src/` files:**
    * `src/workflow.py` -> `euterpe/main_workflow.py` (as a class)
    * `src/config.py` -> logic incorporated into `euterpe/config_loader.py` and `euterpe/models.py` (for `EuterpeConfig`)
    * `src/dify_enhancer.py` -> `euterpe/enhancers/dify_client.py`
    * `src/keyframe_processor.py` -> `euterpe/processors/keyframe_rules.py`
    * `src/image_generator.py` -> `euterpe/generators/image_module.py`
    * `src/music_generator.py` -> `euterpe/generators/music_module.py`
    * `src/video_generator.py` -> `euterpe/generators/video_assembler.py`
9.  **Imports:**
    * Within the `euterpe` package, use absolute imports: `from euterpe.generators import image_module` or `from euterpe.models import Keyframe`.
    * Relative imports (`from . import sibling_module` or `from .. import parent_package_module`) can be used within sub-packages if preferred for closely related modules.
10. **No `main.py` inside `euterpe/` package:** The old `main.py` (command-line entry point) should either be moved to `examples/` if it's for demonstration, or a new CLI entry point can be defined in `pyproject.toml` pointing to a function (e.g., `euterpe.cli:main_cli_func`).

Adherence to this structure is crucial for creating a maintainable and standard Python package.