"""Image generation module for the Euterpe library.

This module interfaces with the KlingDemo library for image generation.
"""

import asyncio
import concurrent.futures
import logging
import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any, Union, List

from pydantic import BaseModel, Field

# Import KlingDemo components from our vendors package
from ..vendors.klingdemo.api import KlingAPIClient
from ..vendors.klingdemo.models import ImageGenerationRequest
KLINGDEMO_AVAILABLE = True

# Set up logger
logger = logging.getLogger(__name__)


class KlingImageResult:
    """Mock result class for when KlingDemo is not available."""
    def __init__(self, task_id, images=None):
        self.task_id = task_id
        self.task_result = self
        self.images = images or [KlingImage("http://example.com/image.png")]


class KlingImage:
    """Mock image class for when KlingDemo is not available."""
    def __init__(self, url):
        self.url = url


class ImageGeneratorConfig(BaseModel):
    """Configuration for the image generator."""
    api_key: Optional[str] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    base_url: str = Field(default="https://api.klingai.com")
    timeout: int = 60
    max_retries: int = 3
    output_dir: Path = Field(default=Path("./output/images"))
    mock_mode: bool = Field(default=False, description="Use mock implementation instead of real API calls")

    class Config:
        validate_assignment = True


class ImageGenerator:
    """Generate images using the KlingDemo library."""
    
    def __init__(self, config: ImageGeneratorConfig):
        """Initialize the image generator.
        
        Args:
            config: Configuration for the image generator.
        """
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize client if KlingDemo is available and we're not in mock mode
        self.client = None
        if KLINGDEMO_AVAILABLE and not self.config.mock_mode:
            try:
                self.client = KlingAPIClient(
                    api_key=self.config.api_key,
                    access_key=self.config.access_key,
                    secret_key=self.config.secret_key,
                    base_url=self.config.base_url,
                    timeout=self.config.timeout,
                    max_retries=self.config.max_retries,
                )
                logger.info("Initialized KlingDemo client for image generation")
            except Exception as e:
                logger.error(f"Failed to initialize KlingDemo client: {e}")
                logger.warning("Falling back to mock implementation")
                self.config.mock_mode = True
        else:
            logger.warning("KlingDemo library not available or mock mode enabled")
            if not KLINGDEMO_AVAILABLE:
                logger.warning("Install the KlingDemo package to enable actual image generation")
            self.config.mock_mode = True
            
    async def generate(
        self,
        prompt: str,
        model_name: str = "kling-v1-5",
        negative_prompt: Optional[str] = None,
        aspect_ratio: str = "16:9",
        seed: Optional[int] = None,
        frame_id: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        steps: Optional[int] = 30,
        cfg_scale: Optional[float] = 7.0,
    ) -> Optional[Path]:
        """Generate an image using the KlingDemo library.
        
        Args:
            prompt: Text prompt for image generation.
            model_name: The model to use for generation.
            negative_prompt: Optional negative prompt.
            aspect_ratio: Image aspect ratio.
            seed: Optional random seed for reproducibility.
            frame_id: Optional frame identifier.
            width: Optional width of the image.
            height: Optional height of the image.
            steps: Number of diffusion steps.
            cfg_scale: Guidance scale.
            
        Returns:
            Path: Path to the generated image file, or None if generation failed.
            
        Raises:
            Exception: If image generation fails.
        """
        try:
            # Generate a safe frame ID from the prompt if not provided
            if not frame_id:
                # Create a safe filename from the first few words of the prompt
                words = prompt.split()[:3]
                frame_id = "_".join(w.lower() for w in words if w.isalnum())
                frame_id = f"img_{frame_id}"
            
            if self.config.mock_mode:
                # Mock implementation
                logger.info(f"[MOCK MODE] Generating image for prompt: {prompt[:30]}...")
                await asyncio.sleep(1)  # Simulate API delay
                
                # Create a simple colored rectangle as a mock image
                from PIL import Image, ImageDraw, ImageFont
                import random
                
                # Define image size based on aspect ratio
                if aspect_ratio == "1:1":
                    img_width, img_height = 512, 512
                elif aspect_ratio == "16:9":
                    img_width, img_height = 512, 288
                elif aspect_ratio == "9:16":
                    img_width, img_height = 288, 512
                else:
                    img_width, img_height = 512, 512
                
                # Override with explicit dimensions if provided
                if width and height:
                    img_width, img_height = width, height
                
                # Create mock image with a random color
                color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                img = Image.new('RGB', (img_width, img_height), color=color)
                draw = ImageDraw.Draw(img)
                
                # Add some text to the image
                draw.text((10, 10), f"Mock: {prompt[:20]}...", fill=(255, 255, 255))
                draw.text((10, 30), f"Model: {model_name}", fill=(255, 255, 255))
                draw.text((10, 50), f"Frame: {frame_id}", fill=(255, 255, 255))
                
                # Save the image
                output_path = self.config.output_dir / f"{frame_id}.png"
                img.save(output_path)
                
                logger.info(f"[MOCK MODE] Generated mock image at {output_path}")
                return output_path
            else:
                # Real implementation
                logger.info(f"Generating image for prompt: {prompt[:30]}...")
                
                # Create image generation request
                request = ImageGenerationRequest(
                    model_name=model_name,
                    prompt=prompt,
                    negative_prompt=negative_prompt or "",
                    n=1,
                    aspect_ratio=aspect_ratio,
                    seed=seed,
                    width=width,
                    height=height,
                    steps=steps,
                    cfg_scale=cfg_scale
                )
                
                # Submit image generation task
                task = self.client.create_image_generation_task(request)
                logger.info(f"Image generation task created with ID: {task.task_id}")
                
                # Wait for task completion - Run blocking method in a thread pool
                def run_task_wait():
                    return self.client.wait_for_image_generation_completion(task.task_id)
                
                # Use run_in_executor to run the blocking operation in a thread pool
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    completed_task = await asyncio.get_event_loop().run_in_executor(
                        pool, run_task_wait
                    )
                
                # Save image locally
                if completed_task.task_result and completed_task.task_result.images:
                    image_url = completed_task.task_result.images[0].url
                    
                    # Use frame_id in the filename
                    filename = f"{frame_id}.png"
                    output_path = self.config.output_dir / filename
                    
                    # Download the image
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
            logger.debug(traceback.format_exc())
            
            # Return None in case of failure
            return None
    
    async def generate_batch(
        self, 
        prompts: List[Dict[str, Any]]
    ) -> List[Optional[Path]]:
        """Generate multiple images in parallel.
        
        Args:
            prompts: List of dictionaries containing generation parameters.
                Each dict should have keys matching the parameters of the generate() method.
                
        Returns:
            List[Optional[Path]]: List of paths to generated images, with None for failed generations.
        """
        # Create tasks for all prompts
        tasks = []
        for p in prompts:
            task = self.generate(
                prompt=p["prompt"],
                model_name=p.get("model_name", "kling-v1-5"),
                negative_prompt=p.get("negative_prompt"),
                aspect_ratio=p.get("aspect_ratio", "16:9"),
                seed=p.get("seed"),
                frame_id=p.get("frame_id"),
                width=p.get("width"),
                height=p.get("height"),
                steps=p.get("steps", 30),
                cfg_scale=p.get("cfg_scale", 7.0),
            )
            tasks.append(task)
        
        # Run all tasks concurrently
        return await asyncio.gather(*tasks)
