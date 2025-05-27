"""Minimal example of using the Euterpe library.

This example demonstrates the simplest possible usage of the Euterpe library.
"""

import os
from pathlib import Path

from euterpe import (
    generate_video,
    VideoGenerationRequest, 
    EuterpeConfig, 
    Keyframe,
    AspectRatio,
    MusicParams,
)

def main():
    """Run a minimal Euterpe example."""
    # Set API keys (in production, use environment variables)
    os.environ["KLING_API_KEY"] = "your_kling_api_key"  # Replace with your key
    os.environ["BEATOVEN_API_KEY"] = "your_beatoven_api_key"  # Replace with your key
    
    # Create output directory
    output_dir = Path("./euterpe_minimal_output")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create a simple configuration
    config = EuterpeConfig(output_dir=output_dir)
    
    # Create keyframes with minimal options
    keyframes = [
        Keyframe(
            timestamp=0.0,
            prompt="A beautiful beach at sunrise, golden light, waves gently touching the shore",
        ),
        Keyframe(
            timestamp=5.0,
            prompt="Beach at midday, bright blue sky, clear water, white sand",
        ),
        Keyframe(
            timestamp=10.0,
            prompt="Beach at sunset, dramatic colors, red and orange sky",
        ),
    ]
    
    # Create music parameters
    music_params = MusicParams(
        prompt="Relaxing calm ocean sounds with soft piano melody",
        duration=15.0,
    )
    
    # Create the request with minimal parameters
    request = VideoGenerationRequest(
        keyframes=keyframes,
        output_filename="minimal_beach_video",
        music_params=music_params,
    )
    
    print("Generating video with minimal configuration...")
    
    # Generate the video
    result = generate_video(request, config)
    
    # Check and print results
    if result.success:
        print(f"\n✅ Video generated successfully at: {result.video_filepath}")
    else:
        print(f"\n❌ Video generation failed: {result.message}")

if __name__ == "__main__":
    main()
