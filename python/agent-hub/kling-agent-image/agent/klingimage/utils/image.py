"""
Utility functions for image handling in KlingDemo.

This module provides helper functions for common image operations 
required for the Kling AI API, such as encoding images to base64.
"""
import base64
import os
from pathlib import Path
from typing import Optional, Union

import requests
from loguru import logger


class ImageError(Exception):
    """Exception raised for errors in image operations."""
    pass


def encode_image_to_base64(image_path: Union[str, Path]) -> str:
    """
    Encode an image file to base64 format.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string of the image (without prefix)

    Raises:
        ImageError: If the file doesn't exist or cannot be read
    """
    try:
        path = Path(image_path)
        if not path.exists():
            raise ImageError(f"Image file not found: {path}")
        
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_string
    except Exception as e:
        raise ImageError(f"Failed to encode image: {e}")


def download_image(url: str, output_path: Optional[Union[str, Path]] = None) -> Union[str, bytes]:
    """
    Download an image from a URL.

    Args:
        url: URL of the image to download
        output_path: Path to save the downloaded image (optional)

    Returns:
        If output_path is provided: the path to the saved image
        Otherwise: the image content as bytes

    Raises:
        ImageError: If the download fails
    """
    try:
        logger.debug(f"Downloading image from {url}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Check if it's an image
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            raise ImageError(f"URL does not point to an image: {content_type}")
        
        # Save to file if output_path is provided
        if output_path:
            path = Path(output_path)
            # Create directory if it doesn't exist
            os.makedirs(path.parent, exist_ok=True)
            
            with open(path, 'wb') as f:
                f.write(response.content)
            logger.debug(f"Image saved to {path}")
            return str(path)
        else:
            return response.content
    except requests.RequestException as e:
        raise ImageError(f"Failed to download image: {e}")
    except Exception as e:
        raise ImageError(f"Error handling image: {e}")


def url_to_base64(url: str) -> str:
    """
    Download an image from a URL and convert it to base64.

    Args:
        url: URL of the image to download

    Returns:
        Base64 encoded string of the image (without prefix)

    Raises:
        ImageError: If the download or encoding fails
    """
    try:
        logger.debug(f"Converting image from URL to base64: {url}")
        image_data = download_image(url)
        encoded_string = base64.b64encode(image_data).decode("utf-8")
        return encoded_string
    except Exception as e:
        raise ImageError(f"Failed to convert URL to base64: {e}")