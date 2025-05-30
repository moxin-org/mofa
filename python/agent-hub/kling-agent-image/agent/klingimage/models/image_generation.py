"""
Models for the Kling AI Image Generation API.

This module contains Pydantic models that represent the request and
response data structures for the Kling AI API, specifically for the
image generation functionality (both text-to-image and image-to-image).
"""
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl, field_validator


# Reuse TaskStatus from image2video module
from .image2video import TaskStatus


class ImageReference(str, Enum):
    """Enum representing possible image reference types for image-to-image generation."""
    SUBJECT = "subject"  # For character/subject features reference
    FACE = "face"        # For human face reference


class ImageResult(BaseModel):
    """Information about a generated image."""
    index: int = Field(..., description="Index of the generated image (starts from 0)")
    url: HttpUrl = Field(..., description="URL where the image can be accessed")


class ImageGenerationTaskResult(BaseModel):
    """Task result containing generated images."""
    images: List[ImageResult] = Field(
        [], 
        description="List of generated images"
    )


class ImageGenerationResponse(BaseModel):
    """Response from creating or retrieving an image generation task."""
    code: int = Field(..., description="Response code, 0 means success")
    message: str = Field(..., description="Response message")
    request_id: str = Field(..., description="Unique request identifier")
    data: Union[Dict, List[Dict]] = Field(..., description="Response data")


class ImageGenerationTaskResponseData(BaseModel):
    """Data returned from a task creation or status check."""
    task_id: str = Field(..., description="Unique task identifier")
    task_status: TaskStatus = Field(..., description="Current status of the task")
    task_status_msg: Optional[str] = Field(None, description="Additional status details")
    created_at: int = Field(..., description="Task creation timestamp (Unix ms)")
    updated_at: int = Field(..., description="Task last updated timestamp (Unix ms)")
    task_result: Optional[ImageGenerationTaskResult] = Field(None, description="Task results (when successful)")


class ImageGenerationRequest(BaseModel):
    """Request body for creating an image generation task."""
    model_name: str = Field(
        default="kling-v1", 
        description="Model name to use for generation",
        pattern="^kling-v[0-9](-[0-9])?$"
    )
    prompt: str = Field(
        ...,
        description="Positive text prompt describing the desired image content",
        max_length=500
    )
    negative_prompt: Optional[str] = Field(
        None,
        description="Negative text prompt describing content to avoid",
        max_length=200
    )
    image: Optional[str] = Field(
        None,
        description="Base64 encoded image or URL to reference image (for image-to-image)"
    )
    image_reference: Optional[ImageReference] = Field(
        None,
        description="Image reference type (required for kling-v1-5 with image)"
    )
    image_fidelity: float = Field(
        default=0.5,
        description="Image reference strength (higher means more adherence to reference image)",
        ge=0,
        le=1
    )
    human_fidelity: float = Field(
        default=0.45,
        description="Face reference strength (only applicable when image_reference is 'face')",
        ge=0,
        le=1
    )
    n: int = Field(
        default=1,
        description="Number of images to generate",
        ge=1,
        le=9
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="Aspect ratio of the generated images"
    )
    callback_url: Optional[HttpUrl] = Field(
        None,
        description="URL to receive task status updates"
    )

    @field_validator('aspect_ratio')
    def validate_aspect_ratio(cls, v):
        """Validate the aspect ratio format and value."""
        valid_ratios = ["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "21:9"]
        if v not in valid_ratios:
            raise ValueError(f"Invalid aspect ratio. Must be one of: {', '.join(valid_ratios)}")
        return v
    
    @field_validator('image_reference')
    def validate_image_reference_requirements(cls, v, info):
        """
        Ensure that image_reference is provided when using kling-v1-5 model with an image.
        """
        if not hasattr(info.context, 'data'):
            return v
            
        data = info.context.data
        model_name = data.get('model_name', "kling-v1")
        has_image = data.get('image') is not None
        
        # For kling-v1-5 with image, image_reference is required
        if model_name == "kling-v1-5" and has_image and v is None:
            raise ValueError("image_reference is required when using kling-v1-5 model with an image")
            
        return v
    
    @field_validator('negative_prompt')
    def validate_negative_prompt_with_image(cls, v, info):
        """
        Ensure that negative_prompt is not used with image-to-image generation.
        """
        if not hasattr(info.context, 'data') or v is None:
            return v
            
        data = info.context.data
        has_image = data.get('image') is not None
        
        if has_image and v is not None:
            raise ValueError("negative_prompt is not supported in image-to-image generation")
            
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "model_name": "kling-v1-5",
                    "prompt": "A beautiful mountain landscape with a lake",
                    "negative_prompt": "blurry, low quality",
                    "n": 1,
                    "aspect_ratio": "16:9"
                }
            ]
        }
    }