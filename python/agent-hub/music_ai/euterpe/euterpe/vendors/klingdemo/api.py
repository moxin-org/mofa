"""
Simplified Kling AI API client implementation for Euterpe.
"""
import json
import logging
import time
from typing import Dict, List, Optional, Union

import requests

from .models import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImageGenerationTaskResponseData,
    TaskStatus,
)

# Set up logger
logger = logging.getLogger("klingdemo")


class KlingAPIError(Exception):
    """Exception raised for errors returned by the Kling AI API."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(self.message)


class NetworkError(KlingAPIError):
    """Exception raised for network-related errors."""
    pass


class ResourceExhaustionError(KlingAPIError):
    """Exception raised when the API returns resource exhaustion errors."""
    pass


class KlingAPIClient:
    """
    Client for interacting with the Kling AI API.
    
    This is a simplified version integrated directly into Euterpe.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.kling.ai",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        """
        Initialize the Kling AI API client.
        
        Args:
            api_key: Kling AI API key for authentication.
            base_url: Base URL for the Kling AI API.
            timeout: Request timeout in seconds.
            max_retries: Maximum number of retries for failed requests.
            retry_delay: Initial delay between retries in seconds (will increase exponentially).
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Verify API key is provided
        if not api_key:
            logger.warning("No API key provided. The client will not be able to make authenticated requests.")
    
    def _generate_auth_headers(self) -> Dict[str, str]:
        """
        Generate authentication headers for API requests.
        
        Returns:
            Dict[str, str]: Headers containing authentication information.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """
        Handle API response and extract JSON data or raise appropriate exceptions.
        
        Args:
            response: Response from the API.
            
        Returns:
            Dict: JSON response data.
            
        Raises:
            KlingAPIError: For API errors with known status codes.
            NetworkError: For network-related errors.
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            status_code = getattr(response, "status_code", None)
            
            try:
                response_body = response.json()
            except Exception:
                response_body = {"raw": response.text} if hasattr(response, "text") else None
            
            if status_code == 429:
                raise ResourceExhaustionError(
                    "API rate limit exceeded. Please try again later.",
                    status_code=status_code,
                    response_body=response_body,
                )
            elif status_code and 400 <= status_code < 500:
                raise KlingAPIError(
                    f"Client error: {e}",
                    status_code=status_code,
                    response_body=response_body,
                )
            elif status_code and 500 <= status_code < 600:
                raise KlingAPIError(
                    f"Server error: {e}",
                    status_code=status_code,
                    response_body=response_body,
                )
            else:
                raise NetworkError(
                    f"Network error: {e}",
                    status_code=status_code,
                    response_body=response_body,
                )
    
    def generate_images(
        self, request: Union[Dict, ImageGenerationRequest]
    ) -> ImageGenerationResponse:
        """
        Generate images using the Kling API.
        
        Args:
            request: Image generation request parameters.
            
        Returns:
            ImageGenerationResponse: Response containing task ID and status.
            
        Raises:
            KlingAPIError: If the API request fails.
        """
        if not self.api_key:
            raise KlingAPIError("API key is required for image generation")
        
        # Handle dict or model input
        if isinstance(request, dict):
            request_data = request
        else:
            request_data = request.dict(exclude_none=True)
        
        endpoint = f"{self.base_url}/v1/images/generation"
        headers = self._generate_auth_headers()
        
        # Simplified mock implementation 
        logger.info(f"Generating images with prompt: {request_data.get('prompt', '')}")
        
        # Simulate a successful API response
        mock_response = {
            "code": 0,
            "message": "Success",
            "data": {
                "task_id": f"mock-{int(time.time())}-{id(request_data)}",
                "status": "waiting"
            }
        }
        
        return ImageGenerationResponse(**mock_response)
    
    def get_task_status(self, task_id: str) -> ImageGenerationResponse:
        """
        Check the status of an image generation task.
        
        Args:
            task_id: The ID of the task to check.
            
        Returns:
            ImageGenerationResponse: Response containing task status and 
                                    result if completed.
            
        Raises:
            KlingAPIError: If the API request fails.
        """
        if not self.api_key:
            raise KlingAPIError("API key is required to check task status")
        
        endpoint = f"{self.base_url}/v1/images/tasks/{task_id}"
        headers = self._generate_auth_headers()
        
        # Simplified mock implementation
        logger.info(f"Checking status for task ID: {task_id}")
        
        # Simulate a completed task
        mock_response = {
            "code": 0,
            "message": "Success",
            "data": {
                "task_id": task_id,
                "status": "completed",
                "result": {
                    "images": [
                        {
                            "index": 0,
                            "url": f"https://example.com/images/{task_id}_0.jpg"
                        }
                    ]
                }
            }
        }
        
        return ImageGenerationResponse(**mock_response)
    
    def generate_images_and_wait(
        self,
        request: Union[Dict, ImageGenerationRequest],
        timeout: int = 120,
        polling_interval: int = 2,
    ) -> List[str]:
        """
        Generate images and wait for the task to complete.
        
        Args:
            request: Image generation request parameters.
            timeout: Maximum time to wait in seconds.
            polling_interval: Time between status checks in seconds.
            
        Returns:
            List[str]: URLs of the generated images.
            
        Raises:
            KlingAPIError: If the API request fails.
            TimeoutError: If the task doesn't complete within the timeout period.
        """
        # Start the generation task
        response = self.generate_images(request)
        
        if not response.data or not response.data.task_id:
            raise KlingAPIError("Failed to start image generation task")
            
        task_id = response.data.task_id
        start_time = time.time()
        
        # Poll until completion or timeout
        while time.time() - start_time < timeout:
            # Get task status
            status_response = self.get_task_status(task_id)
            
            # Check if task has completed or failed
            if status_response.data and status_response.data.status == TaskStatus.COMPLETED:
                if (status_response.data.result and 
                    status_response.data.result.images):
                    # Return the URLs of generated images
                    return [img.url for img in status_response.data.result.images]
                else:
                    raise KlingAPIError("Task completed but no images were returned")
                    
            elif status_response.data and status_response.data.status == TaskStatus.FAILED:
                raise KlingAPIError(f"Image generation failed: {status_response.message}")
            
            # Wait before checking again
            time.sleep(polling_interval)
        
        # If we get here, the task has timed out
        raise TimeoutError(f"Image generation timed out after {timeout} seconds")
