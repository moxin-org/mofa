"""Public API for the Euterpe library.

This module provides the main entry point for the Euterpe video generation library.
"""

import logging
import traceback
import sys
from typing import Optional, Dict, Any

from .models import VideoGenerationRequest, VideoGenerationResult, EuterpeConfig
from .main_workflow import EuterpeWorkflow
from .config_loader import load_config

# Set up logger
logger = logging.getLogger(__name__)

# Configure a null handler to prevent "No handler found" warnings
logger.addHandler(logging.NullHandler())


def generate_video(
    request: VideoGenerationRequest, config: Optional[EuterpeConfig] = None
) -> VideoGenerationResult:
    """Generate a video from keyframes and optional music.

    This is the main entry point for the Euterpe library. It orchestrates the entire
    video generation process from keyframes and optional music.

    Args:
        request: The video generation request with all user-configurable parameters.
        config: Optional configuration with API keys and settings. If not provided,
            a default configuration will be loaded from environment variables.

    Returns:
        VideoGenerationResult: A result object containing success status, file paths and messages.

    Example:
        ```python
        from euterpe import generate_video, VideoGenerationRequest, Keyframe

        # Create keyframes
        keyframes = [
            Keyframe(
                frame_id="frame1",
                timestamp=0.0,
                prompt="A beautiful sunrise over mountains",
            ),
            Keyframe(
                frame_id="frame2",
                timestamp=5.0,
                prompt="Sun rising higher in the sky",
            )
        ]

        # Create request
        request = VideoGenerationRequest(
            keyframes=keyframes,
            music_prompt="Peaceful ambient music",
            output_filename="sunrise_video"
        )

        # Generate video
        result = generate_video(request)

        if result.success:
            print(f"Video generated at: {result.video_filepath}")
        else:
            print(f"Error: {result.message}")
        ```
    """
    try:
        # Load config if not provided
        if config is None:
            logger.info("No configuration provided, loading default configuration")
            config = load_config()
        
        # Initialize workflow
        logger.info("Initializing EuterpeWorkflow")
        workflow = EuterpeWorkflow(config=config)
        
        # Process request
        logger.info(f"Processing video generation request with {len(request.keyframes)} keyframes")
        result = workflow.process(request)
        
        # Log successful completion
        if result.success:
            logger.info(
                f"Video generation completed successfully: {result.video_filepath}"
            )
        
        return result
    
    except Exception as e:
        # Get detailed traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        # Log the error with traceback
        logger.error(f"Error in generate_video: {str(e)}")
        logger.debug(f"Traceback: {tb_str}")
        
        # Return error result with detailed error information
        return VideoGenerationResult(
            success=False,
            message=f"Video generation failed: {type(e).__name__}",
            error_details=f"{str(e)}\n\nTraceback:\n{tb_str}",
            metadata={"error_type": str(type(e).__name__)}
        )
