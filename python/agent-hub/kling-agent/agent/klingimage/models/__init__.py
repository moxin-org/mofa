"""
Data models for the Kling AI API.
"""
from .image2video import (
    CameraControl, 
    CameraControlConfig,
    DynamicMask, 
    ImageToVideoRequest, 
    ImageToVideoResponse, 
    TaskInfo,
    TaskResponseData, 
    TaskResult, 
    TaskStatus, 
    TrajectoryPoint, 
    VideoResult
)

from .image_generation import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    ImageGenerationTaskResponseData,
    ImageGenerationTaskResult,
    ImageReference,
    ImageResult
)

__all__ = [
    # Image-to-Video models
    "CameraControl", 
    "CameraControlConfig",
    "DynamicMask", 
    "ImageToVideoRequest", 
    "ImageToVideoResponse", 
    "TaskInfo",
    "TaskResponseData", 
    "TaskResult", 
    "TaskStatus", 
    "TrajectoryPoint", 
    "VideoResult",
    
    # Image Generation models
    "ImageGenerationRequest",
    "ImageGenerationResponse",
    "ImageGenerationTaskResponseData",
    "ImageGenerationTaskResult",
    "ImageReference",
    "ImageResult"
]