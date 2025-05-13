# Euterpe Tests

This directory contains automated tests for the Euterpe library.

## Test Structure

- `test_api.py`: Tests for the main API entry points (e.g., `generate_video()`)
- `test_workflow.py`: Tests for the `EuterpeWorkflow` class and execution flow
- `test_models.py`: Tests for Pydantic models and their validation

## Running Tests

From the project root directory:

```bash
pytest
```

For more verbose output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_api.py
```

To run a specific test:

```bash
pytest tests/test_api.py::test_generate_video_success
```

## Test Dependencies

Tests require:

- pytest
- pytest-asyncio (for async tests)
- unittest.mock (for mocking external services)

Install with:

```bash
pip install pytest pytest-asyncio
```

## Writing New Tests

- All tests should use mocking for external services (Beatoven, Kling, ffmpeg, etc.)
- Use pytest fixtures for common test data and setup
- Follow the pattern of existing tests for consistency
- Use descriptive test names and docstrings
