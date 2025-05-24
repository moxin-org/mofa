"""
Video generation module using the KlingDemo API.
"""
import asyncio
import concurrent.futures
import logging
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Import KlingDemo components
from klingdemo.api import KlingAPIClient
from klingdemo.models import ImageToVideoRequest

logger = logging.getLogger(__name__)

class VideoGenerator:
    """Handles video generation from images using the KlingDemo API."""
    
    def __init__(self, kling_config: Dict[str, Any], output_dir: Path):
        """
        Initialize the video generator with API credentials.
        
        Args:
            kling_config: Configuration for the KlingAPIClient
            output_dir: Directory to save generated videos
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
        logger.info("Initialized video generator with KlingDemo client")
    
    async def generate_from_image(self, image_path: Path, prompt: str, frame_id: str, 
                                 mode: str = "std", duration: str = "5",
                                 model_name: str = "kling-v1") -> Optional[Path]:
        """
        Generate a video from an image using the KlingDemo API.
        
        Args:
            image_path: Path to the input image
            prompt: Text prompt describing the desired video
            frame_id: Identifier for the generated frame
            mode: Video generation mode ("std" or other options)
            duration: Video duration in seconds as a string
            model_name: Model to use for generation
            
        Returns:
            Path to the generated video, or None if generation failed
        """
        try:
            # Properly encode the image file to base64
            with open(image_path, "rb") as image_file:
                import base64
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create image-to-video request
            request = ImageToVideoRequest(
                model_name=model_name,
                image=encoded_image,
                prompt=prompt,
                mode=mode,
                duration=duration
            )
            
            # Submit image-to-video task
            task = self.client.create_image_to_video_task(request)
            logger.info(f"Video generation task created with ID: {task.task_id}")
            
            # Custom polling logic to handle potential validation errors
            max_wait_time = 300  # 5 minutes max wait time
            check_interval = 5   # Check every 5 seconds
            elapsed = 0
            
            # Define task status check function for thread pool
            def get_task_status():
                try:
                    response = self.client._request("GET", f"/v1/videos/image2video/{task.task_id}")
                    return response
                except Exception as e:
                    logger.error(f"Error getting task status: {e}")
                    raise
            
            # Wait for the task to complete with polling
            completed_task = None
            while elapsed < max_wait_time:
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    response = await asyncio.get_event_loop().run_in_executor(pool, get_task_status)
                
                # Extract status from response directly
                if "data" in response:
                    data = response["data"]
                    
                    # Check for task_status in data
                    if isinstance(data, dict) and "task_status" in data:
                        status = data["task_status"]
                        logger.info(f"Task {task.task_id} status: {status}")
                        
                        if status == "succeed":
                            logger.info(f"Task {task.task_id} completed successfully")
                            completed_task = data
                            break
                        elif status == "failed":
                            error_msg = data.get("task_status_msg", "Unknown error")
                            logger.error(f"Task {task.task_id} failed: {error_msg}")
                            return None
                
                # Sleep before next check
                await asyncio.sleep(check_interval)
                elapsed += check_interval
            else:
                # Timed out
                logger.warning(f"Timeout waiting for video generation task {task.task_id}")
                return None
            
            # Process completed task result
            if completed_task and "task_result" in completed_task and completed_task["task_result"]:
                task_result = completed_task["task_result"]
                
                if "videos" in task_result and task_result["videos"]:
                    videos = task_result["videos"]
                    if videos and len(videos) > 0 and isinstance(videos[0], dict) and "url" in videos[0]:
                        video_url = videos[0]["url"]
                        output_path = self.output_dir / f"{frame_id}.mp4"
                        
                        # Download the video
                        import requests
                        response = requests.get(video_url)
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        
                        logger.info(f"Video downloaded to {output_path}")
                        return output_path
            
            logger.warning(f"No video generated for task {task.task_id}")
            return None
            
        except Exception as e:
            logger.error(f"Error generating video: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None