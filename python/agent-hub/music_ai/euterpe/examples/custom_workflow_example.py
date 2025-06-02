"""Example of using the Euterpe library with a custom workflow.

This example demonstrates how to create a custom workflow that extends
the default EuterpeWorkflow to add additional functionality.

It also shows how to access the vendor modules directly when needed for
more advanced use cases. The BeatovenAI and KlingDemo libraries are now
integrated directly into Euterpe as vendor modules, eliminating the need
for separate installation.
"""

import os
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any

from euterpe import EuterpeConfig, VideoGenerationRequest, VideoGenerationResult
from euterpe.main_workflow import EuterpeWorkflow
from euterpe.models import Keyframe, AspectRatio

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("euterpe-custom-workflow")


class CustomEuterpeWorkflow(EuterpeWorkflow):
    """Custom workflow that extends the default EuterpeWorkflow with additional features."""
    
    def __init__(self, config: Optional[EuterpeConfig] = None, request: Optional[VideoGenerationRequest] = None):
        """Initialize the custom workflow.
        
        Args:
            config: Optional configuration with API keys and settings.
            request: Optional video generation request.
        """
        super().__init__(config, request)
        self.watermark_enabled = True
        logger.info("Custom workflow initialized with watermarking enabled")
        
    async def run(self) -> Dict[str, Any]:
        """Override the run method to add custom processing.
        
        Returns:
            Dict[str, Any]: Dictionary with paths to generated files and metadata.
        """
        logger.info("Running custom workflow")
        
        # Add a custom step before the standard workflow
        if self.request:
            self._preprocess_keyframes()
        
        # Call the parent method to run the standard workflow
        result_data = await super().run()
        
        # Add a custom post-processing step
        if self.watermark_enabled and result_data.get('image_filepaths'):
            result_data = self._add_watermarks(result_data)
        
        return result_data
    
    def _preprocess_keyframes(self) -> None:
        """Add custom preprocessing for keyframes."""
        logger.info("Preprocessing keyframes in custom workflow")
        
        # For demonstration, add a prefix to all prompts
        style_prefix = "High quality, detailed, photorealistic, "
        for keyframe in self.request.keyframes:
            if not keyframe.prompt.startswith(style_prefix):
                keyframe.prompt = style_prefix + keyframe.prompt
                logger.debug(f"Updated prompt for keyframe {keyframe.frame_id}")
    
    def _add_watermarks(self, result_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate adding watermarks to generated images."""
        logger.info("Adding watermarks to generated images")
        
        # In a real implementation, this would add actual watermarks to the images
        # For this example, we're just adding a note to the metadata
        
        if 'metadata' not in result_data:
            result_data['metadata'] = {}
            
        result_data['metadata']['watermarked'] = True
        result_data['metadata']['watermark_text'] = "Generated with Custom Euterpe"
        
        return result_data

    def use_vendor_modules_directly(self):
        """Demonstrate direct access to vendor modules for advanced use cases."""
        logger.info("Accessing vendor modules directly within the custom workflow")

        # Example: Using KlingDemo vendor module
        from euterpe.vendors.klingdemo.api import KlingAPIClient
        from euterpe.vendors.klingdemo.models import ImageGenerationRequest

        kling_client = KlingAPIClient(api_key=os.environ.get("KLING_API_KEY"))
        image_request = ImageGenerationRequest(
            prompt="A futuristic cityscape at night, neon lights, high detail",
            negative_prompt="blurry, low quality",
            width=1024,
            height=768,
            num_images=1,
            guidance_scale=7.5,
            steps=40,
        )
        logger.info("Generating image using KlingDemo vendor module")
        image_data = kling_client.generate_image(image_request)

        # Example: Using BeatovenAI vendor module
        from euterpe.vendors.beatoven_ai.client import BeatovenClient
        from euterpe.vendors.beatoven_ai.models import TrackRequest, TextPrompt

        beatoven_client = BeatovenClient(api_key=os.environ.get("BEATOVEN_API_KEY"))
        music_request = TrackRequest(
            prompt=TextPrompt(text="Epic orchestral music with a sense of adventure"),
            duration_seconds=30.0,
            genre="orchestral",
            tempo=120,
        )
        logger.info("Generating music using BeatovenAI vendor module")
        music_data = beatoven_client.generate_track(music_request)

        logger.info("Vendor module usage demonstration complete")


def create_sample_request() -> VideoGenerationRequest:
    """Create a sample video generation request."""
    # Create sample keyframes
    keyframes = [
        Keyframe(
            frame_id="scene1",
            timestamp=0.0,
            prompt="Ocean waves crashing on a rocky shore at dawn",
            aspect_ratio=AspectRatio.LANDSCAPE.value,
        ),
        Keyframe(
            frame_id="scene2",
            timestamp=5.0,
            prompt="Lighthouse on a cliff overlooking the ocean",
            aspect_ratio=AspectRatio.LANDSCAPE.value,
        ),
        Keyframe(
            frame_id="scene3",
            timestamp=10.0,
            prompt="Close-up of seagulls flying over the ocean at sunset",
            aspect_ratio=AspectRatio.LANDSCAPE.value,
        ),
    ]
    
    # Create and return the request
    return VideoGenerationRequest(
        keyframes=keyframes,
        music_prompt="Calming ocean waves sound with gentle piano",
        output_filename="ocean_journey",
    )


def main():
    """Main function to run the example."""
    # Set up API keys (replace with your own keys in a real application)
    if not os.environ.get("KLING_API_KEY"):
        os.environ["KLING_API_KEY"] = "your_kling_api_key"
    if not os.environ.get("BEATOVEN_API_KEY"):
        os.environ["BEATOVEN_API_KEY"] = "your_beatoven_api_key"
    
    # Create output directory
    output_dir = Path("./euterpe_custom_output")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Create configuration
    config = EuterpeConfig(
        output_dir=output_dir,
    )
    
    # Create request
    request = create_sample_request()
    
    print(f"Generating video using custom workflow")
    print(f"Output directory: {output_dir}")
    
    try:
        # Initialize custom workflow
        workflow = CustomEuterpeWorkflow(config=config, request=request)
        
        # Process the request
        result = workflow.process()
        
        # Print results
        if result.success:
            print("\n✅ Video generated successfully!")
            print(f"🎬 Video filepath: {result.video_filepath}")
            if result.metadata and 'watermarked' in result.metadata:
                print(f"🔒 Watermark added: {result.metadata['watermark_text']}")
        else:
            print("\n❌ Video generation failed!")
            print(f"Error message: {result.message}")
    
    except Exception as e:
        print(f"Error running custom workflow: {e}")


if __name__ == "__main__":
    main()