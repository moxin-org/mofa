#!/usr/bin/env python
"""
Basic demonstration of the KlingDemo client library.

This script shows how to use the KlingDemo client to create an
image-to-video generation task and retrieve the result.
"""
import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

# Add the parent directory to the path to allow importing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from klingdemo.api import KlingAPIClient, KlingAPIError, NetworkError
from klingdemo.models import ImageToVideoRequest, TaskStatus
from klingdemo.utils import (
    ConfigurationError,
    encode_image_to_base64,
    load_config,
    setup_logging,
)
from loguru import logger


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Demo for the KlingDemo client library for image-to-video generation"
    )
    parser.add_argument(
        "--image", "-i", 
        type=str, 
        required=True, 
        help="Path to the input image file or image URL"
    )
    parser.add_argument(
        "--prompt", "-p", 
        type=str, 
        default=None, 
        help="Text description of the desired video (optional)"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        type=str,
        default=None,
        help="Text description of content to avoid (optional)"
    )
    parser.add_argument(
        "--model", "-m", 
        type=str, 
        default="kling-v1", 
        choices=["kling-v1", "kling-v1-5", "kling-v1-6"],
        help="Model to use (default: kling-v1)"
    )
    parser.add_argument(
        "--mode", 
        type=str, 
        default="std", 
        choices=["std", "pro"],
        help="Generation mode (default: std)"
    )
    parser.add_argument(
        "--duration", "-d", 
        type=str, 
        default="5", 
        choices=["5", "10"],
        help="Video duration in seconds (default: 5)"
    )
    parser.add_argument(
        "--cfg-scale", "-c", 
        type=float, 
        default=0.5,
        help="Generation freedom factor (0-1, default: 0.5)"
    )
    parser.add_argument(
        "--output", "-o", 
        type=str, 
        default="./output", 
        help="Directory to save the output video (default: ./output)"
    )
    parser.add_argument(
        "--env-file", "-e", 
        type=str, 
        default=None, 
        help="Path to .env file containing API key"
    )
    parser.add_argument(
        "--log-level", "-l", 
        type=str, 
        default="INFO", 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )
    parser.add_argument(
        "--timeout", "-t", 
        type=int, 
        default=300,
        help="Maximum time to wait for task completion in seconds (default: 300)"
    )
    
    return parser.parse_args()


def is_url(s: str) -> bool:
    """Check if a string is a URL."""
    return s.startswith(('http://', 'https://'))


def save_video(url: str, output_dir: str) -> str:
    """
    Download and save a video from a URL.
    
    Args:
        url: URL to the video file
        output_dir: Directory to save the video
    
    Returns:
        Path to the saved video file
    """
    import requests
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract filename from URL or use a default name
    try:
        filename = os.path.basename(url.split('?')[0])
        if not filename or '.' not in filename:
            filename = f"video_{int(time.time())}.mp4"
    except Exception:
        filename = f"video_{int(time.time())}.mp4"
    
    output_path = os.path.join(output_dir, filename)
    
    # Download the video
    logger.info(f"Downloading video from {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Save the video
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    logger.info(f"Video saved to {output_path}")
    return output_path


def main(args: Optional[argparse.Namespace] = None):
    """
    Run the demo.
    
    Args:
        args: Command line arguments (optional, will parse if not provided)
    """
    if args is None:
        args = parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    try:
        # Load configuration from environment variables or .env file
        config = load_config(args.env_file)
        
        # Create API client
        client = KlingAPIClient(
            access_key=config['access_key'],
            secret_key=config['secret_key'],
            base_url=config.get('api_base_url', 'https://api.klingai.com'),
            timeout=config.get('timeout', 60),
            max_retries=config.get('max_retries', 3),
            token_expiration=config.get('token_expiration', 1800)
        )
        
        # Prepare image data
        logger.info(f"Processing input image: {args.image}")
        if is_url(args.image):
            image = args.image  # Pass URL directly
        else:
            # Encode local file to base64
            image = encode_image_to_base64(args.image)
            logger.debug("Image encoded to base64")
        
        # Prepare request
        request = ImageToVideoRequest(
            model_name=args.model,
            image=image,
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            cfg_scale=args.cfg_scale,
            mode=args.mode,
            duration=args.duration,
            external_task_id=f"demo_{int(time.time())}",  # Generate a unique ID
        )
        
        # Submit the task
        logger.info("Submitting image-to-video generation task...")
        task = client.create_image_to_video_task(request)
        logger.info(f"Task created with ID: {task.task_id}")
        
        # Wait for task to complete
        logger.info("Waiting for task to complete...")
        start_time = time.time()
        try:
            task = client.wait_for_task_completion(
                task.task_id,
                check_interval=5,
                timeout=args.timeout
            )
            elapsed = time.time() - start_time
            logger.info(f"Task completed in {elapsed:.1f} seconds")
            
            # Process results
            if task.task_status == TaskStatus.SUCCEED and task.task_result:
                for i, video in enumerate(task.task_result.videos):
                    logger.info(f"Video {i+1}: {video.url}")
                    # Save the video
                    saved_path = save_video(str(video.url), args.output)
                    logger.info(f"Video saved to {saved_path}")
            else:
                logger.error(f"Task failed with status: {task.task_status}")
                if task.task_status_msg:
                    logger.error(f"Error message: {task.task_status_msg}")
                    
        except TimeoutError:
            logger.error(f"Task timed out after {args.timeout} seconds")
            # Get the final status
            task = client.get_task_by_id(task.task_id)
            logger.info(f"Final task status: {task.task_status}")
            
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except KlingAPIError as e:
        logger.error(f"API error: {e}")
        if hasattr(e, 'request_id') and e.request_id:
            logger.error(f"Request ID: {e.request_id}")
        sys.exit(1)
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()