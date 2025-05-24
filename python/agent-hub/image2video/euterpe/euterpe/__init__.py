"""Euterpe - A Python lfrom .enhancers import DifyClient, DifyEnhancerConfig
from .generators import (
    ImageGenerator, 
    ImageGeneratorConfig,
    MusicGenerator, 
    MusicGeneratorConfig,
    VideoAssembler, 
    VideoAssemblerConfig
)
from .processors import KeyframeProcessororchestrate AI-driven video generation from keyframes.

This package provides tools for generating videos from keyframes using AI services.
"""

__version__ = "0.1.0"

# Export the main public API elements
from .api import generate_video
from .models import (
    VideoGenerationRequest,
    VideoGenerationResult,
    EuterpeConfig,
    Keyframe,
    AspectRatio,
    ImageGenerationParams,
    VideoOutputParams,
    MusicParams,
    ImageModel,
    DifyEnhancementParams,
)

# Export important types from subpackages
from .enhancers import DifyClient, DifyEnhancerConfig
from .generators import (
    ImageGenerator, 
    ImageGeneratorConfig,
    MusicGenerator, 
    MusicGeneratorConfig,
    VideoAssembler, 
    VideoAssemblerConfig,
)
from .processors import KeyframeProcessor

__all__ = [
    # Main API
    "generate_video",
    
    # Core models
    "VideoGenerationRequest",
    "VideoGenerationResult",
    "EuterpeConfig",
    "Keyframe",
    
    # Configuration models    "AspectRatio",
    "ImageGenerationParams",
    "VideoOutputParams",
    "MusicParams",
    "ImageModel",
    "DifyEnhancementParams",
    
    # Enhancers
    "DifyClient",
    "DifyEnhancerConfig",
    
    # Generators
    "ImageGenerator",
    "ImageGeneratorConfig",
    "MusicGenerator",
    "MusicGeneratorConfig",
    "VideoAssembler",
    "VideoAssemblerConfig",
    
    # Processors
    "KeyframeProcessor",
    
    # Version
    "__version__",
]
