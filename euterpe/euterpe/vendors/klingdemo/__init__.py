"""Kling Demo vendor module integrated into Euterpe.

This module contains the core functionality from the KlingDemo package
integrated directly into Euterpe for simplified usage.
"""

from euterpe.vendors.klingdemo.api import KlingAPIClient, KlingAPIError, NetworkError, ResourceExhaustionError
from euterpe.vendors.klingdemo.models import (
    ImageGenerationRequest, 
    ImageGenerationResponse,
    ImageGenerationTaskResponseData,
    TaskStatus,
    ImageResult
)

__all__ = [
    "KlingAPIClient", 
    "KlingAPIError", 
    "NetworkError", 
    "ResourceExhaustionError",
    "ImageGenerationRequest", 
    "ImageGenerationResponse",
    "ImageGenerationTaskResponseData",
    "TaskStatus",
    "ImageResult"
]
