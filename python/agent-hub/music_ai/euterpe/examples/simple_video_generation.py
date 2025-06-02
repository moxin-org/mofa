"""Comprehensive example of using the Euterpe library.

This example demonstrates how to use the Euterpe library to generate a video
from keyframes with various configurations and options. All dependencies, including
the previously separate BeatovenDemo and KlingDemo libraries, are now directly
integrated into the Euterpe package for simplified usage.
"""

import os
import logging
from pathlib import Path
import argparse
from typing import List, Optional

from euterpe import (
    generate_video,
    VideoGenerationRequest,
    VideoGenerationResult,
    EuterpeConfig,
    Keyframe,
    AspectRatio,
    ImageGenerationParams,
    VideoOutputParams,
    MusicParams,
    DifyEnhancementParams,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("euterpe-example")

def setup_environment() -> None:
    """Set up environment variables for API keys.
    
    In a production environment, these should be set through a secure
    environment variable management system or config files.
    
    Note: The BeatovenDemo and KlingDemo libraries are now integrated
    directly into Euterpe as vendor modules, but still require API keys.
    """
    # Check if API keys are already set in environment
    if not os.environ.get("KLING_API_KEY"):
        logger.warning("KLING_API_KEY not found in environment, using placeholder")
        os.environ["KLING_API_KEY"] = "your_kling_api_key"  # Replace with your key
    
    if not os.environ.get("BEATOVEN_API_KEY"):
        logger.warning("BEATOVEN_API_KEY not found in environment, using placeholder")
        os.environ["BEATOVEN_API_KEY"] = "your_beatoven_api_key"  # Replace with your key
    
    if not os.environ.get("DIFY_API_KEY"):
        logger.info("DIFY_API_KEY not found in environment, prompt enhancement will be disabled")
        # This is optional, so we won't set a placeholder

def create_sample_keyframes() -> List[Keyframe]:
    """Create a list of sample keyframes for the video."""
    # Common negative prompt for all keyframes
    negative_prompt = "blurry, low quality, distorted, ugly, text, watermark"
    
    return [
        Keyframe(
            frame_id="sunrise_start",
            timestamp=0.0,
            prompt="A beautiful sunrise over mountains, orange and pink sky, golden glow on horizon",
            negative_prompt=negative_prompt,
            aspect_ratio=AspectRatio.LANDSCAPE.value,
            seed=12345,  # Using fixed seed for reproducibility
        ),
        Keyframe(
            frame_id="sunrise_mid",
            timestamp=5.0,
            prompt="Sun rising higher over mountains, landscape illuminated with golden light, long shadows",
            negative_prompt=negative_prompt,
            aspect_ratio=AspectRatio.LANDSCAPE.value,
            seed=12345,  # Same seed for style consistency
        ),
        Keyframe(
            frame_id="daylight_scene",
            timestamp=10.0,
            prompt="Full daylight mountain landscape with blue sky, snow-capped peaks, vibrant colors",
            negative_prompt=negative_prompt,
            aspect_ratio=AspectRatio.LANDSCAPE.value,
            seed=12345,  # Same seed for style consistency
        ),
        Keyframe(
            frame_id="sunset_scene",
            timestamp=15.0,
            prompt="Mountain sunset with dramatic clouds, red and orange sky, silhouettes of mountains",
            negative_prompt=negative_prompt,
            aspect_ratio=AspectRatio.LANDSCAPE.value,
            seed=12345,  # Same seed for style consistency
        ),
    ]

def create_video_request(output_name: str, enhance_prompts: bool = False) -> VideoGenerationRequest:
    """Create a sample video generation request."""
    # Create image generation parameters
    image_params = ImageGenerationParams(
        model_name="kling-v2",  # Using the latest model
        negative_prompt="blurry, low quality, distorted, ugly, text, watermark",
        aspect_ratio=AspectRatio.LANDSCAPE.value,
        cfg_scale=7.5,  # Slightly higher guidance scale for more prompt adherence
        steps=40,  # More diffusion steps for higher quality
    )
    
    # Create video parameters
    video_params = VideoOutputParams(
        filename=output_name,
        fps=24.0,
        format="mp4",
        include_audio=True,
    )
    
    # Create music parameters
    music_params = MusicParams(
        prompt="Peaceful orchestral music with piano and strings, emotional, inspirational, journey through nature",
        duration=20.0,  # Match our video length
        genre="ambient",
        tempo=85,  # Medium tempo
    )
    
    # Create enhancement parameters if enabled
    enhancement_params = None
    if enhance_prompts:
        enhancement_params = DifyEnhancementParams(
            enabled=True,
            enhancement_level="detailed",
            context_keywords=["nature", "mountains", "cinematic", "beautiful"],
        )
    
    # Create and return the request
    return VideoGenerationRequest(
        keyframes=create_sample_keyframes(),
        music_params=music_params,
        output_filename=output_name,
        video_params=video_params,
        enhance_prompts=enhance_prompts,
        enhancement_params=enhancement_params,
        default_image_params=image_params,
    )

def print_result_details(result: VideoGenerationResult) -> None:
    """Print details about the video generation result."""
    if result.success:
        print("\n✅ Video generated successfully!")
        print(f"🎬 Video filepath: {result.video_filepath}")
        print(f"🎵 Music filepath: {result.music_filepath}")
        print(f"🖼️ Generated {len(result.image_filepaths)} images")
        
        if result.metadata:
            print("\n📊 Metadata:")
            for key, value in result.metadata.items():
                print(f"  - {key}: {value}")
    else:
        print("\n❌ Video generation failed!")
        print(f"Error message: {result.message}")
        if result.error_details:
            print(f"Error details: {result.error_details}")

def main():
    """Main function to run the example."""
    parser = argparse.ArgumentParser(description="Generate a video using Euterpe.")
    parser.add_argument("--output", default="mountain_journey", help="Base name for output files")
    parser.add_argument("--enhance", action="store_true", help="Enable prompt enhancement")
    parser.add_argument("--output-dir", default="./euterpe_output", help="Output directory")
    parser.add_argument("--show-vendor-info", action="store_true", help="Show information about vendor modules")
    args = parser.parse_args()
    
    # Display vendor module information if requested
    if args.show_vendor_info:
        print("Euterpe uses integrated vendor modules:")
        print("- beatoven_ai: Music generation (integrated directly)")
        print("- klingdemo: Image generation (integrated directly)")
        print("These modules are now part of the Euterpe package and don't need separate installation.")
    
    # Setup environment
    setup_environment()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create configuration
    config = EuterpeConfig(
        output_dir=output_dir,
        use_dify_enhancement=args.enhance,
        max_retries=5,  # More retries for better resilience
        request_timeout=120,  # Longer timeout for larger images
    )
    
    # Create request
    request = create_video_request(args.output, args.enhance)
    
    print(f"Generating video '{args.output}' with {len(request.keyframes)} keyframes")
    print(f"Output directory: {output_dir}")
    
    # Generate the video
    result = generate_video(request, config)
    
    # Print results
    print_result_details(result)

if __name__ == "__main__":
    main()
