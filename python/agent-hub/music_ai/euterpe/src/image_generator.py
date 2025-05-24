"""
Image generation module using the KlingDemo API.
"""
import asyncio
import concurrent.futures
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Import KlingDemo components
from klingdemo.api import KlingAPIClient
from klingdemo.models import ImageGenerationRequest

logger = logging.getLogger(__name__)

class ImageGenerator:
    """Handles image generation using the KlingDemo API."""
    
    def __init__(self, kling_config: Dict[str, Any], output_dir: Path):
        """
        Initialize the image generator with API credentials.
        
        Args:
            kling_config: Configuration for the KlingAPIClient
            output_dir: Directory to save generated images
        """
        self.output_dir = output_dir
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize KlingAPIClient
        self.client = KlingAPIClient(
            access_key=kling_config.get('access_key'),
            secret_key=kling_config.get('secret_key'),
            base_url=kling_config.get('api_base_url', 'https://api.klingai.com'),
            timeout=kling_config.get('timeout', 60),
            max_retries=kling_config.get('max_retries', 3),
        )
        logger.info("Initialized image generator with KlingDemo client")
    
    async def generate(self, prompt: str, model_name: str = "kling-v1-5", 
                      negative_prompt: str = "", aspect_ratio: str = "16:9", 
                      seed: Optional[int] = None, frame_id: str = None) -> Optional[Path]:
        """
        Generate an image using the KlingDemo API.
        
        Args:
            prompt: Text prompt describing the desired image
            model_name: Model to use for generation
            negative_prompt: Elements to avoid in the image
            aspect_ratio: Image aspect ratio (e.g., "16:9")
            seed: Random seed for reproducibility
            frame_id: Identifier for the generated frame
            
        Returns:
            Path to the generated image, or None if generation failed
        """
        try:
            # Create image generation request
            request = ImageGenerationRequest(
                model_name=model_name,
                prompt=prompt,
                negative_prompt=negative_prompt,
                n=1,
                aspect_ratio=aspect_ratio,
                seed=seed
            )
            
            # Submit image generation task
            task = self.client.create_image_generation_task(request)
            logger.info(f"Image generation task created with ID: {task.task_id}")
            
            # Wait for task completion - Run blocking method in a thread pool
            def run_task_wait():
                return self.client.wait_for_image_generation_completion(task.task_id)
            
            # Use run_in_executor to run the blocking operation in a thread pool
            with concurrent.futures.ThreadPoolExecutor() as pool:
                completed_task = await asyncio.get_event_loop().run_in_executor(pool, run_task_wait)
            
            # Save image locally
            if completed_task.task_result and completed_task.task_result.images:
                image_url = completed_task.task_result.images[0].url
                
                # Use frame_id in the filename if provided
                filename = f"{frame_id}.png" if frame_id else f"image_{task.task_id}.png"
                output_path = self.output_dir / filename
                
                # Download the image
                import requests
                response = requests.get(image_url)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                
                logger.info(f"Image downloaded to {output_path}")
                return output_path
            
            logger.warning(f"No images generated for task {task.task_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None