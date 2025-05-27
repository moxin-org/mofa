# Euterpe Tests

This directory contains automated tests for the Euterpe library.

## Test Status

✅ **All tests passing!** (21 tests)

## Test Structure

- `test_api.py`: Tests for the main API entry points (e.g., `generate_video()`) - ✅ 4 tests
- `test_workflow.py`: Tests for the `EuterpeWorkflow` class and execution flow - ✅ 5 tests
- `test_models.py`: Tests for Pydantic models and their validation - ✅ 12 tests

## Test Details

### API Tests
- ✅ `test_generate_video_returns_result` - Tests the basic function call returns a result
- ✅ `test_generate_video_success` - Tests successful video generation with mocks
- ✅ `test_generate_video_failure` - Tests error handling during generation
- ✅ `test_generate_video_default_config` - Tests default config creation

### Workflow Tests
- ✅ `test_run_calls_components_in_order` - Tests component execution order
- ✅ `test_run_with_image_generation_failure` - Tests error handling
- ✅ `test_run_with_dify_enhancement` - Tests prompt enhancement
- ✅ `test_run_with_music_disabled` - Tests workflow without music
- ✅ `test_run_with_custom_output_directory` - Tests custom directory usage

### Model Tests
- ✅ `test_keyframe_basic_creation` - Tests basic Keyframe model initialization
- ✅ `test_keyframe_with_all_fields` - Tests Keyframe model with all optional fields
- ✅ `test_keyframe_validates_timestamp` - Tests timestamp validation
- ✅ `test_keyframe_validates_prompt_length` - Tests prompt length validation
- ✅ `test_basic_request_creation` - Tests basic VideoGenerationRequest creation
- ✅ `test_request_with_all_fields` - Tests VideoGenerationRequest with all fields
- ✅ `test_request_validates_keyframes_not_empty` - Tests keyframes validation
- ✅ `test_request_sorts_keyframes_by_timestamp` - Tests automatic keyframe sorting
- ✅ `test_config_default_values` - Tests EuterpeConfig default values
- ✅ `test_config_custom_values` - Tests EuterpeConfig custom values
- ✅ `test_result_successful` - Tests successful VideoGenerationResult
- ✅ `test_result_failure` - Tests failed VideoGenerationResult

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

## Recent Fixes

### API Test Fixes
- Fixed mocking approach in API tests by using `process()` instead of `run()`
- Corrected result object creation with proper VideoGenerationResult instances
- Fixed assertion checks for error handling tests

### Workflow Test Fixes
- Updated method names in mocks from `generate_images` to `generate` to match implementation
- Created custom test implementations to work with frozen Pydantic models
- Properly mocked async methods and functions with AsyncMock
- Implemented workarounds for model modification attempts by creating new instances

### Implementation Fixes
- Added proper handling for music duration in `main_workflow.py`
- Fixed `video_duration` attribute error by using `music_params.duration`
- Improved error handling and validation across components

## Writing New Tests

- All tests should use mocking for external services (Beatoven, Kling, ffmpeg, etc.)
- Use pytest fixtures for common test data and setup
- Follow the pattern of existing tests for consistency
- Use descriptive test names and docstrings
- When testing async functions, use `pytest.mark.asyncio` and AsyncMock
- When working with frozen Pydantic models, create new instances rather than attempting to modify

## Known Issues

- There are some deprecation warnings related to Pydantic V1 style validators that could be updated in future
- The custom event_loop fixture in conftest.py will need updating in future pytest-asyncio versions
