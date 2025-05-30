#!/usr/bin/env python
"""
Image Generation Demo for the Kling AI API.

This script demonstrates how to use the KlingDemo library to generate images
using either text-to-image or image-to-image capabilities.
"""
import argparse
import json
import os
import sys
import time
from base64 import b64encode
from pathlib import Path
from typing import Optional

from loguru import logger

from klingdemo.api import KlingAPIClient, ResourceExhaustionError
from klingdemo.models import ImageGenerationRequest, ImageReference
from klingdemo.utils import load_config, setup_logging


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to base64 for API submission.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string of the image (without any prefix)
    """
    try:
        with open(image_path, "rb") as img_file:
            return b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to encode image: {e}")
        sys.exit(1)


def setup_arg_parser() -> argparse.ArgumentParser:
    """
    Set up command line argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Image Generation Demo for Kling AI API",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # General parameters
    parser.add_argument(
        "--model", 
        type=str, 
        default="kling-v1",
        choices=["kling-v1", "kling-v1-5", "kling-v2"],
        help="Model to use for image generation"
    )
    parser.add_argument(
        "--prompt", 
        type=str, 
        required=True,
        help="Text prompt describing the desired image content"
    )
    parser.add_argument(
        "--negative-prompt", 
        type=str,
        help="Text describing what to avoid in the generated image"
    )
    parser.add_argument(
        "--n", 
        type=int, 
        default=1,
        choices=range(1, 10),
        help="Number of images to generate (1-9)"
    )
    parser.add_argument(
        "--aspect-ratio", 
        type=str, 
        default="16:9",
        choices=["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "21:9"],
        help="Aspect ratio of the generated image"
    )
    
    # Image-to-image parameters
    parser.add_argument(
        "--image", 
        type=str, 
        help="Path to reference image file or URL (for image-to-image generation)"
    )
    parser.add_argument(
        "--image-reference", 
        type=str,
        choices=["subject", "face"],
        help="How to use the reference image (subject features or face reference)"
    )
    parser.add_argument(
        "--image-fidelity", 
        type=float, 
        default=0.5,
        help="Image reference strength (0-1, higher means more adherence to reference)"
    )
    parser.add_argument(
        "--human-fidelity", 
        type=float, 
        default=0.45,
        help="Face reference strength (0-1, higher means more similarity to reference face)"
    )
    
    # Output parameters
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="./output",
        help="Directory to save generated images"
    )
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=300,
        help="Maximum time to wait for task completion in seconds"
    )
    parser.add_argument(
        "--log-level", 
        type=str, 
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level"
    )
    parser.add_argument(
        "--env-file", 
        type=str, 
        help="Path to .env file with API credentials"
    )
    parser.add_argument(
        "--no-fallback", 
        action="store_true",
        help="Disable fallback attempts when resources are exhausted"
    )
    
    return parser


def create_request_with_fallbacks(args, client: KlingAPIClient):
    """
    Create and submit an image generation request with fallback options if resources are exhausted.
    
    Args:
        args: Command line arguments
        client: KlingAPIClient instance
        
    Returns:
        The task response data if successful
        
    Raises:
        ResourceExhaustionError: If all fallback attempts fail
    """
    # Process image if provided
    image = None
    if args.image:
        if args.image.startswith(("http://", "https://")):
            logger.info(f"Using image URL: {args.image}")
            image = args.image  # Pass URL directly
        else:
            # Encode local file to base64
            logger.info(f"Using local image: {args.image}")
            image = encode_image_to_base64(args.image)
            logger.debug("Image encoded to base64")
    
    # Creating the image reference if needed
    image_reference = None
    if args.image_reference:
        if args.image_reference == "subject":
            image_reference = ImageReference.SUBJECT
        elif args.image_reference == "face":
            image_reference = ImageReference.FACE
    
    # Define our fallback strategies
    fallback_options = []
    
    # Original request (with user's parameters)
    original_params = {
        "model_name": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "aspect_ratio": args.aspect_ratio,
    }
    
    if args.negative_prompt and not image:
        original_params["negative_prompt"] = args.negative_prompt
    
    if image:
        original_params["image"] = image
        
    if image_reference:
        original_params["image_reference"] = image_reference
        
    if image:
        original_params["image_fidelity"] = args.image_fidelity
        
    if image_reference == ImageReference.FACE:
        original_params["human_fidelity"] = args.human_fidelity
    
    fallback_options.append(original_params)
    
    # Only add fallbacks if not disabled
    if not args.no_fallback:
        # Fallback 1: Same request but with n=1 (just one image)
        if args.n > 1:
            fallback1 = dict(original_params)
            fallback1["n"] = 1
            fallback_options.append(fallback1)
        
        # Fallback 2: Use kling-v1 model (simplest model) with n=1
        if args.model != "kling-v1":
            fallback2 = dict(original_params)
            fallback2["model_name"] = "kling-v1"
            fallback2["n"] = 1
            fallback_options.append(fallback2)
    
    # Try each option in sequence until one works
    last_error = None
    for i, params in enumerate(fallback_options):
        try:
            if i > 0:
                logger.warning(f"Attempting fallback option {i}: {params}")
            
            # Create request object and submit
            request = ImageGenerationRequest(**params)
            task = client.create_image_generation_task(request)
            logger.info(f"Task created with ID: {task.task_id}")
            return task
            
        except ResourceExhaustionError as e:
            last_error = e
            logger.warning(f"Resources exhausted with option {i}: {e}")
            # Log detailed error information
            logger.debug(f"Error details - Status: {e.status_code}, Error code: {e.error_code}, Request ID: {e.request_id}")
            if hasattr(e, 'raw_response') and e.raw_response:
                logger.debug(f"Raw response: {json.dumps(e.raw_response)}")
    
    # If we get here, all attempts failed
    if last_error:
        logger.error("All attempts to create task failed due to resource exhaustion")
        logger.error(f"Last error: {last_error}")
        raise last_error
    else:
        raise ResourceExhaustionError("Failed to create image generation task")


def main(args: Optional[argparse.Namespace] = None):
    """
    Main function for the image generation demo.

    Args:
        args: Command line arguments (optional, will parse from sys.argv if None)
    """
    if args is None:
        parser = setup_arg_parser()
        args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    try:
        # Load configuration from environment or .env file
        config = load_config(args.env_file)
        
        # Create API client
        client = KlingAPIClient(
            access_key=config["access_key"],
            secret_key=config["secret_key"],
            base_url=config["api_base_url"],
            timeout=config["timeout"],
            max_retries=config["max_retries"]
        )
        
        # Create and submit the task with fallback options if needed
        try:
            task = create_request_with_fallbacks(args, client)
        except ResourceExhaustionError as e:
            logger.error("Resource pack exhausted. Please try:")
            logger.error(" - Using the basic kling-v1 model instead of advanced models")
            logger.error(" - Generating fewer images (--n=1)")
            logger.error(" - Waiting for your resource quota to refresh")
            logger.error(" - Contacting Kling AI support to increase your quota")
            sys.exit(1)
        
        # Wait for task to complete
        logger.info("Waiting for task to complete...")
        start_time = time.time()
        try:
            task = client.wait_for_image_generation_completion(
                task.task_id,
                check_interval=5,
                timeout=args.timeout
            )
            elapsed = time.time() - start_time
            logger.info(f"Task completed in {elapsed:.1f} seconds")
            
            # Process results
            if not task.task_result:
                logger.error("Task completed but no results were returned")
                sys.exit(1)
                
            # Create output directory if it doesn't exist
            output_dir = Path(args.output_dir)
            output_dir.mkdir(exist_ok=True, parents=True)
            
            # Download and save all generated images
            logger.info(f"Generated {len(task.task_result.images)} images:")
            for img in task.task_result.images:
                # Get the image URL
                image_url = str(img.url)
                image_index = img.index
                
                # Determine a filename based on task ID and image index
                output_filename = f"{task.task_id}_{image_index}.png"
                output_path = output_dir / output_filename
                
                logger.info(f"Image {image_index}: {image_url}")
                logger.info(f"  > Saving to: {output_path}")
                
                # We could download the image here, but let's just print the URL
                # to keep this example simple
                
                # Optional: Download the image
                try:
                    import requests
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        with open(output_path, "wb") as f:
                            f.write(response.content)
                        logger.info(f"  > Downloaded successfully")
                    else:
                        logger.warning(f"  > Failed to download: HTTP {response.status_code}")
                except Exception as e:
                    logger.warning(f"  > Failed to download: {e}")
        
        except TimeoutError:
            logger.error(f"Task timed out after {args.timeout} seconds")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()