#!/usr/bin/env python
"""
Advanced demonstration of the KlingDemo client library.

This script shows how to use the advanced features of the Kling AI API,
such as dynamic masks, static masks, and camera control.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional, Dict

# Add the parent directory to the path to allow importing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from klingdemo.api import KlingAPIClient, KlingAPIError, NetworkError
from klingdemo.models import (
    CameraControl, 
    CameraControlConfig, 
    DynamicMask, 
    ImageToVideoRequest, 
    TaskStatus, 
    TrajectoryPoint
)
from klingdemo.utils import (
    ConfigurationError,
    ImageError,
    encode_image_to_base64,
    load_config,
    setup_logging,
    url_to_base64,
)
from loguru import logger


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Advanced demo for the KlingDemo client with dynamic masks and camera control"
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
        "--model", "-m", 
        type=str, 
        default="kling-v1", 
        choices=["kling-v1", "kling-v1-5", "kling-v1-6"],
        help="Model to use (default: kling-v1)"
    )
    parser.add_argument(
        "--mode", 
        type=str, 
        default="pro", 
        choices=["std", "pro"],
        help="Generation mode (default: pro - required for advanced features)"
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
        "--feature", "-f", 
        type=str, 
        required=True,
        choices=["dynamic_mask", "static_mask", "camera_control", "image_tail"],
        help="Advanced feature to demonstrate"
    )
    parser.add_argument(
        "--static-mask", 
        type=str, 
        help="Path to static mask image file or URL (required for static_mask feature)"
    )
    parser.add_argument(
        "--dynamic-mask", 
        type=str, 
        help="Path to dynamic mask image file or URL (required for dynamic_mask feature)"
    )
    parser.add_argument(
        "--trajectories", 
        type=str, 
        help="JSON array of trajectory points [{'x': int, 'y': int}, ...] (required for dynamic_mask feature)"
    )
    parser.add_argument(
        "--camera-type", 
        type=str, 
        choices=["simple", "down_back", "forward_up", "right_turn_forward", "left_turn_forward"],
        help="Camera control type (required for camera_control feature)"
    )
    parser.add_argument(
        "--camera-param", 
        type=str, 
        choices=["horizontal", "vertical", "pan", "tilt", "roll", "zoom"],
        help="Camera parameter to use for 'simple' camera type"
    )
    parser.add_argument(
        "--camera-value", 
        type=float, 
        help="Value for the camera parameter (-10 to 10)"
    )
    parser.add_argument(
        "--image-tail", 
        type=str, 
        help="Path to tail image file or URL (required for image_tail feature)"
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
        default=600,
        help="Maximum time to wait for task completion in seconds (default: 600)"
    )
    
    return parser.parse_args()


def is_url(s: str) -> bool:
    """Check if a string is a URL."""
    return s.startswith(('http://', 'https://'))


def prepare_image_input(image_path: str) -> str:
    """
    Prepare image input for the API.
    
    Args:
        image_path: Path or URL to the image
        
    Returns:
        Image data as URL or base64-encoded string
    """
    if is_url(image_path):
        return image_path
    else:
        return encode_image_to_base64(image_path)


def parse_trajectories(trajectories_json: str) -> List[TrajectoryPoint]:
    """
    Parse trajectories from JSON string.
    
    Args:
        trajectories_json: JSON string containing trajectory points
        
    Returns:
        List of TrajectoryPoint objects
    """
    try:
        data = json.loads(trajectories_json)
        return [TrajectoryPoint(x=point["x"], y=point["y"]) for point in data]
    except (json.JSONDecodeError, KeyError) as e:
        raise ValueError(f"Invalid trajectories format: {e}")


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


def get_camera_control(camera_type: str, param: Optional[str] = None, value: Optional[float] = None) -> CameraControl:
    """
    Create a camera control configuration.
    
    Args:
        camera_type: Type of camera movement
        param: Camera parameter (for 'simple' type)
        value: Parameter value (for 'simple' type)
        
    Returns:
        CameraControl object
    """
    if camera_type == "simple":
        if not param or value is None:
            raise ValueError("Camera parameter and value are required for 'simple' camera type")
            
        # Create a config with all zeros
        config_params = {
            "horizontal": 0.0,
            "vertical": 0.0,
            "pan": 0.0,
            "tilt": 0.0,
            "roll": 0.0,
            "zoom": 0.0
        }
        
        # Set the specified parameter
        if param not in config_params:
            raise ValueError(f"Invalid camera parameter: {param}")
            
        config_params[param] = float(value)
        camera_config = CameraControlConfig(**config_params)
        return CameraControl(type=camera_type, config=camera_config)
    else:
        # For other types, config is not needed
        return CameraControl(type=camera_type)


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
        
        # Prepare base request
        request_data: Dict = {
            "model_name": args.model,
            "mode": args.mode,
            "prompt": args.prompt,
            "duration": "5",  # Advanced features only support 5s duration
            "external_task_id": f"advanced_demo_{int(time.time())}",
            "image": prepare_image_input(args.image),
        }
        
        # Add advanced feature-specific parameters
        if args.feature == "dynamic_mask":
            if not args.dynamic_mask or not args.trajectories:
                raise ValueError("dynamic-mask and trajectories arguments are required for dynamic_mask feature")
                
            dynamic_mask = prepare_image_input(args.dynamic_mask)
            trajectories = parse_trajectories(args.trajectories)
            
            request_data["dynamic_masks"] = [
                {
                    "mask": dynamic_mask,
                    "trajectories": trajectories
                }
            ]
            logger.info(f"Using dynamic mask with {len(trajectories)} trajectory points")
            
        elif args.feature == "static_mask":
            if not args.static_mask:
                raise ValueError("static-mask argument is required for static_mask feature")
                
            request_data["static_mask"] = prepare_image_input(args.static_mask)
            logger.info("Using static mask")
            
        elif args.feature == "camera_control":
            if not args.camera_type:
                raise ValueError("camera-type argument is required for camera_control feature")
                
            camera_control = get_camera_control(
                args.camera_type, 
                args.camera_param, 
                args.camera_value
            )
            request_data["camera_control"] = camera_control.model_dump(exclude_none=True)
            logger.info(f"Using camera control: {args.camera_type}")
            
        elif args.feature == "image_tail":
            if not args.image_tail:
                raise ValueError("image-tail argument is required for image_tail feature")
                
            request_data["image_tail"] = prepare_image_input(args.image_tail)
            logger.info("Using image tail")
        
        # Create and validate the request
        try:
            request = ImageToVideoRequest(**request_data)
        except Exception as e:
            logger.error(f"Invalid request parameters: {e}")
            sys.exit(1)
            
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
    except ImageError as e:
        logger.error(f"Image error: {e}")
        sys.exit(1)
    except KlingAPIError as e:
        logger.error(f"API error: {e}")
        if hasattr(e, 'request_id') and e.request_id:
            logger.error(f"Request ID: {e.request_id}")
        sys.exit(1)
    except NetworkError as e:
        logger.error(f"Network error: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Value error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()