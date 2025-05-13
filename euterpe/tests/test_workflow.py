"""Tests for the Euterpe Workflow.

This module contains tests for the EuterpeWorkflow class, which is responsible for
coordinating the video generation process.
"""

import os
import asyncio
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from euterpe import (
    VideoGenerationRequest,
    EuterpeConfig,
    Keyframe,
    AspectRatio,
    MusicParams,
    VideoOutputParams,
    ImageGenerationParams,
)
from euterpe.main_workflow import EuterpeWorkflow


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


class TestEuterpeWorkflow:
    """Tests for the EuterpeWorkflow class."""

    @patch('euterpe.main_workflow.ImageGenerator')
    @patch('euterpe.main_workflow.MusicGenerator')
    @patch('euterpe.main_workflow.VideoAssembler')
    @pytest.mark.asyncio
    async def test_run_calls_components_in_order(
        self, 
        MockVideoAssembler, 
        MockMusicGenerator, 
        MockImageGenerator, 
        sample_request, 
        sample_config
    ):
        """Test that the run method calls the components in the correct order."""        # Setup mocks - use correct method names and AsyncMock for all async methods
        mock_image_generator = MockImageGenerator.return_value
        mock_image_generator.generate = AsyncMock()
        mock_image_generator.generate.return_value = "test_output/frame_0000.png"
        
        mock_music_generator = MockMusicGenerator.return_value
        mock_music_generator.generate = AsyncMock()
        mock_music_generator.generate.return_value = "test_output/test_output.mp3"
        
        mock_video_assembler = MockVideoAssembler.return_value
        mock_video_assembler.assemble_video = AsyncMock()
        mock_video_assembler.assemble_video.return_value = "test_output/test_output.mp4"
        
        # Create workflow and run
        workflow = EuterpeWorkflow(config=sample_config, request=sample_request)
        result = await workflow.run()
          # Verify component construction and method calls
        MockImageGenerator.assert_called_once()
        MockMusicGenerator.assert_called_once()
        MockVideoAssembler.assert_called_once()
        
        # Verify the methods were called with the correct method names
        mock_image_generator.generate.assert_called()
        mock_music_generator.generate.assert_called()
        mock_video_assembler.assemble_video.assert_called()
        
        # Verify result
        assert result["success"] is True
        assert result["video_filepath"] == "test_output/test_output.mp4"
        assert result["music_filepath"] == "test_output/test_output.mp3"
        assert len(result["image_filepaths"]) == 2
    
    @patch('euterpe.main_workflow.ImageGenerator')
    @patch('euterpe.main_workflow.MusicGenerator')
    @patch('euterpe.main_workflow.VideoAssembler')
    @pytest.mark.asyncio
    async def test_run_with_image_generation_failure(
        self, 
        MockVideoAssembler, 
        MockMusicGenerator, 
        MockImageGenerator, 
        sample_request, 
        sample_config
    ):
        """Test handling of a failure during image generation."""        # Setup mocks - image generation fails
        mock_image_generator = MockImageGenerator.return_value
        mock_image_generator.generate = AsyncMock()
        mock_image_generator.generate.side_effect = Exception("Image generation failed")
        
        # Create workflow and run
        workflow = EuterpeWorkflow(config=sample_config, request=sample_request)
        result = await workflow.run()
          # Verify component usage
        MockImageGenerator.assert_called_once()
        mock_image_generator.generate.assert_called()
        
        # Music and video assembly shouldn't be called if image generation fails
        MockMusicGenerator.assert_not_called()
        MockVideoAssembler.assert_not_called()
        
        # Verify result reflects failure
        assert result["success"] is False
        assert "image generation failed" in result["error_details"].lower()
    
    @patch('euterpe.main_workflow.ImageGenerator')
    @patch('euterpe.main_workflow.MusicGenerator')
    @patch('euterpe.main_workflow.VideoAssembler')
    @patch('euterpe.main_workflow.DifyClient')
    @pytest.mark.asyncio
    async def test_run_with_dify_enhancement(
        self, 
        MockDifyClient, 
        MockVideoAssembler, 
        MockMusicGenerator, 
        MockImageGenerator, 
        sample_request, 
        sample_config
    ):
        """Test that Dify enhancement is used when enabled."""
        # Create a new config with Dify enhancement enabled
        # We can't modify the existing config since it's frozen
        dify_config = EuterpeConfig(
            output_dir=str(sample_config.output_dir),
            use_dify_enhancement=True,
            max_retries=sample_config.max_retries,
            request_timeout=sample_config.request_timeout,
        )
        
        # Setup mocks
        mock_dify_client = MockDifyClient.return_value
        mock_dify_client.enhance_prompt = MagicMock()  # Not async in the real implementation
        mock_dify_client.enhance_prompt.return_value = "Enhanced prompt"
        
        mock_image_generator = MockImageGenerator.return_value
        mock_image_generator.generate = AsyncMock()
        mock_image_generator.generate.return_value = "test_output/frame_0000.png"
        
        mock_music_generator = MockMusicGenerator.return_value
        mock_music_generator.generate = AsyncMock()
        mock_music_generator.generate.return_value = "test_output/test_output.mp3"
        
        mock_video_assembler = MockVideoAssembler.return_value
        mock_video_assembler.assemble_video = AsyncMock()
        mock_video_assembler.assemble_video.return_value = "test_output/test_output.mp4"
        
        # Create workflow and run
        workflow = EuterpeWorkflow(config=dify_config, request=sample_request)
        result = await workflow.run()
        
        # Verify Dify client was created and used
        MockDifyClient.assert_called_once()
        mock_dify_client.enhance_prompt.assert_called()
        
        # Verify other components were also used
        mock_image_generator.generate.assert_called()
        mock_music_generator.generate.assert_called()
        mock_video_assembler.assemble_video.assert_called()
    
    @patch('euterpe.main_workflow.ImageGenerator')
    @patch('euterpe.main_workflow.MusicGenerator')
    @patch('euterpe.main_workflow.VideoAssembler')
    @pytest.mark.asyncio
    async def test_run_with_music_disabled(
        self, 
        MockVideoAssembler, 
        MockMusicGenerator, 
        MockImageGenerator, 
        sample_request, 
        sample_config
    ):
        """Test that music generation is skipped when disabled."""
        # Create a new request without music params
        # We can't modify the existing request since it's frozen
        music_disabled_request = VideoGenerationRequest(
            keyframes=sample_request.keyframes,
            output_filename=sample_request.output_filename,
            video_params=sample_request.video_params,
            # Omit music_params
        )
        
        # Setup mocks
        mock_image_generator = MockImageGenerator.return_value
        mock_image_generator.generate = AsyncMock()
        mock_image_generator.generate.return_value = "test_output/frame_0000.png"
        
        mock_video_assembler = MockVideoAssembler.return_value
        mock_video_assembler.assemble_video = AsyncMock()
        mock_video_assembler.assemble_video.return_value = "test_output/test_output.mp4"
        
        # Create workflow and run
        workflow = EuterpeWorkflow(config=sample_config, request=music_disabled_request)
        result = await workflow.run()
        
        # Verify music generator was not used
        MockMusicGenerator.assert_not_called()
        
        # Verify other components were used
        mock_image_generator.generate.assert_called()
        mock_video_assembler.assemble_video.assert_called()
        
        # Verify result
        assert result["music_filepath"] is None


    @patch('euterpe.main_workflow.ImageGenerator')
    @patch('euterpe.main_workflow.MusicGenerator')
    @patch('euterpe.main_workflow.VideoAssembler')
    @pytest.mark.asyncio
    async def test_run_with_custom_output_directory(
        self, 
        MockVideoAssembler, 
        MockMusicGenerator, 
        MockImageGenerator, 
        sample_request, 
        sample_config
    ):
        """Test that a custom output directory is created and used."""
        # Create a new config with a custom output directory
        custom_dir = "./custom_test_output"
        custom_config = EuterpeConfig(
            output_dir=custom_dir,
            max_retries=sample_config.max_retries,
            request_timeout=sample_config.request_timeout,
        )
        
        # Setup mocks
        mock_image_generator = MockImageGenerator.return_value
        mock_image_generator.generate = AsyncMock()
        mock_image_generator.generate.return_value = f"{custom_dir}/frame_0000.png"
        
        mock_music_generator = MockMusicGenerator.return_value
        mock_music_generator.generate = AsyncMock()
        mock_music_generator.generate.return_value = f"{custom_dir}/test_output.mp3"
        
        mock_video_assembler = MockVideoAssembler.return_value
        mock_video_assembler.assemble_video = AsyncMock()
        mock_video_assembler.assemble_video.return_value = f"{custom_dir}/test_output.mp4"
        
        # Create workflow and run
        with patch('euterpe.main_workflow.Path.mkdir') as mock_mkdir:
            workflow = EuterpeWorkflow(config=custom_config, request=sample_request)
            result = await workflow.run()
            
            # Verify directory was created
            mock_mkdir.assert_called_with(parents=True, exist_ok=True)
            
            # Verify components were used
            mock_image_generator.generate.assert_called()
            mock_music_generator.generate.assert_called()
            mock_video_assembler.assemble_video.assert_called()
            
            # Verify output paths in result use the custom directory
            assert custom_dir in result["video_filepath"]
            assert custom_dir in result["music_filepath"]
            assert all(custom_dir in path for path in result["image_filepaths"])
