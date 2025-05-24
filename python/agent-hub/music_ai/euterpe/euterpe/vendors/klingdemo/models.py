"""
Simplified models for Kling AI image generation integration in Euterpe.
"""
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, HttpUrl


class TaskStatus(str, Enum):
    """Enum representing possible task statuses."""
    WAITING = "waiting"  # Task is queued
    PROCESSING = "processing"  # Task is being processed
    COMPLETED = "completed"  # Task completed successfully
    FAILED = "failed"  # Task failed


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


class ImageGenerationRequest(BaseModel):
    """Request parameters for generating images from text prompts."""
    prompt: str = Field(
        ..., 
        description="Text prompt describing the image to generate"
    )
    negative_prompt: Optional[str] = Field(
        None, 
        description="Text describing elements to avoid in the generated image"
    )
    width: int = Field(
        1024, 
        description="Width of the generated image in pixels",
        ge=256,
        le=2048
    )
    height: int = Field(
        1024, 
        description="Height of the generated image in pixels",
        ge=256,
        le=2048
    )
    num_images: int = Field(
        1, 
        description="Number of images to generate",
        ge=1,
        le=4
    )
    guidance_scale: float = Field(
        7.5, 
        description="Scale for classifier-free guidance",
        ge=1.0,
        le=20.0
    )
    model: Optional[str] = Field(
        None, 
        description="Model to use for generation (e.g., 'kling-v1-5')"
    )
    steps: int = Field(
        30, 
        description="Number of diffusion steps",
        ge=20,
        le=50
    )
    seed: Optional[int] = Field(
        None, 
        description="Random seed for deterministic generation"
    )


class ImageGenerationTaskResponseData(BaseModel):
    """Data returned from a successful image generation task."""
    task_id: str = Field(..., description="Unique ID of the generation task")
    status: TaskStatus = Field(..., description="Current status of the task")
    result: Optional[ImageGenerationTaskResult] = Field(
        None,
        description="Result containing generated images, only present when status is COMPLETED"
    )


class ImageGenerationResponse(BaseModel):
    """Response from creating or retrieving an image generation task."""
    code: int = Field(..., description="Response code, 0 means success")
    message: str = Field(..., description="Response message")
    data: Optional[ImageGenerationTaskResponseData] = Field(
        None,
        description="Response data, only present on success"
    )
