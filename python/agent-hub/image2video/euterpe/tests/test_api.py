"""Tests for the Euterpe API.

This module contains tests for the main Euterpe API, specifically focusing on
the generate_video function. Tests use mocking to avoid actual service calls.
"""

import os
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from euterpe import (
    generate_video,
    VideoGenerationRequest,
    VideoGenerationResult,
    EuterpeConfig,
    Keyframe,
    AspectRatio,
    MusicParams,
    VideoOutputParams,
    ImageGenerationParams,
)


@pytest.fixture
def sample_request():
    """Create a sample VideoGenerationRequest for testing."""
    return VideoGenerationRequest(
        keyframes=[
            Keyframe(
                frame_id="test_frame",
                timestamp=0.0,
                prompt="Test prompt",
                aspect_ratio=AspectRatio.LANDSCAPE.value,
            ),
            Keyframe(
                frame_id="test_frame_2",
                timestamp=5.0,
                prompt="Another test prompt",
                aspect_ratio=AspectRatio.LANDSCAPE.value,
            ),
        ],
        output_filename="test_output",
        music_params=MusicParams(
            prompt="Test music prompt",
            duration=10.0,
        ),
        video_params=VideoOutputParams(
            fps=24.0,
            format="mp4",
            include_audio=True,
        ),
    )


@pytest.fixture
def sample_config(tmp_path):
    """Create a sample EuterpeConfig for testing."""
    # Use pytest's tmp_path fixture to create a temporary directory
    # This ensures the directory exists for the test
    test_output_dir = tmp_path / "test_output"
    test_output_dir.mkdir(exist_ok=True)
    
    return EuterpeConfig(
        output_dir=str(test_output_dir),
        use_dify_enhancement=False,
        max_retries=2,
        request_timeout=60,
    )


def test_generate_video_returns_result(sample_request):
    """Test that generate_video returns a VideoGenerationResult."""
    # Act
    result = generate_video(sample_request)
    
    # Assert
    assert isinstance(result, VideoGenerationResult)


@patch('euterpe.api.EuterpeWorkflow')
def test_generate_video_success(MockEuterpeWorkflow, sample_request, sample_config):
    """Test successful video generation with mocked workflow."""
    # Setup mock workflow instance and its process method
    mock_workflow_instance = MockEuterpeWorkflow.return_value
    mock_workflow_instance.process = MagicMock()
    mock_workflow_instance.process.return_value = VideoGenerationResult(
        success=True,
        message="Video generated successfully",
        video_filepath="test_output/test_output.mp4",
        music_filepath="test_output/test_output.mp3",
        image_filepaths=["test_output/frame_0000.png", "test_output/frame_0001.png"],
        metadata={
            "duration": 10.0,
            "frames": 2,
        }
    )    # Call the generate_video function with our test fixtures
    result = generate_video(request=sample_request, config=sample_config)

    # Verify the workflow was constructed and called correctly
    MockEuterpeWorkflow.assert_called_once_with(config=sample_config)
    mock_workflow_instance.process.assert_called_once_with(sample_request)
    
    # Verify the result contains the expected values
    assert result.success is True
    assert "successfully" in result.message.lower()
    assert result.video_filepath == "test_output/test_output.mp4"
    assert result.music_filepath == "test_output/test_output.mp3"
    assert len(result.image_filepaths) == 2
    assert result.metadata.get("duration") == 10.0


@patch('euterpe.api.EuterpeWorkflow')
def test_generate_video_failure(MockEuterpeWorkflow, sample_request, sample_config):
    """Test video generation failure handling."""
    # Setup mock workflow to simulate a failure
    mock_workflow_instance = MockEuterpeWorkflow.return_value
    mock_workflow_instance.process = MagicMock()
    mock_workflow_instance.process.side_effect = Exception("Test error message")    # Call the generate_video function
    result = generate_video(request=sample_request, config=sample_config)

    # Verify the workflow was constructed correctly
    MockEuterpeWorkflow.assert_called_once_with(config=sample_config)
      # Verify the result indicates failure
    assert result.success is False
    assert "failed" in result.message.lower()  # "Video generation failed: Exception"
    assert "test error message" in result.error_details.lower()


@patch('euterpe.api.EuterpeWorkflow')
def test_generate_video_default_config(MockEuterpeWorkflow, sample_request):
    """Test that generate_video uses a default config if none is provided."""
    # Setup mock workflow
    mock_workflow_instance = MockEuterpeWorkflow.return_value
    mock_workflow_instance.process = MagicMock()
    mock_workflow_instance.process.return_value = VideoGenerationResult(
        success=True,
        message="Video generated successfully",
        video_filepath="output/video.mp4",
        music_filepath="output/music.mp3",
        image_filepaths=["output/frame_0000.png"],
    )

    # Call generate_video without a config
    result = generate_video(request=sample_request)

    # Verify a default config was created and used
    assert MockEuterpeWorkflow.call_args is not None
    _, kwargs = MockEuterpeWorkflow.call_args
    assert 'config' in kwargs
    assert isinstance(kwargs['config'], EuterpeConfig)
    
    # Verify the result has data from our mock return value
    assert result.success is True  # This should now work with our mocked return value
