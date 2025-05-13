"""Pydantic models for the Euterpe library.

This module defines the data models used throughout the Euterpe library,
including configuration, request and response structures.
"""

import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from pydantic import BaseModel, Field, HttpUrl, DirectoryPath, FilePath, validator


class AspectRatio(str, Enum):
    """Standard aspect ratios for generated images and videos."""
    SQUARE = "1:1"
    PORTRAIT = "9:16"
    LANDSCAPE = "16:9"
    WIDESCREEN = "21:9"
    CINEMA = "2.39:1"


class ImageModel(str, Enum):
    """Available image generation models."""
    KLING_V1 = "kling-v1"
    KLING_V1_5 = "kling-v1-5"
    KLING_V2 = "kling-v2"


class MusicParams(BaseModel):
    """Parameters for music generation."""
    prompt: str = Field(..., description="Text prompt describing the music to generate")
    duration: Optional[float] = Field(
        default=180.0, 
        description="Duration of the music in seconds"
    )
    genre: Optional[str] = Field(
        default=None, 
        description="Specific genre for the music"
    )
    tempo: Optional[int] = Field(
        default=None, 
        description="Tempo in beats per minute"
    )
    format: str = Field(
        default="mp3", 
        description="Output file format (mp3, wav, etc.)"
    )

    class Config:
        frozen = True


class DifyEnhancementParams(BaseModel):
    """Parameters for prompt enhancement using Dify."""
    enabled: bool = Field(
        default=False,
        description="Whether to use Dify for enhancing prompts"
    )
    enhancement_level: str = Field(
        default="standard",
        description="Level of enhancement to apply (minimal, standard, detailed)"
    )
    context_keywords: Optional[List[str]] = Field(
        default=None,
        description="Additional keywords to provide context for enhancement"
    )

    class Config:
        frozen = True


class ImageGenerationParams(BaseModel):
    """Parameters for image generation."""
    model_name: str = Field(
        default=ImageModel.KLING_V1_5.value,
        description="Model to use for image generation"
    )
    negative_prompt: Optional[str] = Field(
        default=None,
        description="Elements to exclude from the generated image"
    )
    aspect_ratio: str = Field(
        default=AspectRatio.LANDSCAPE.value,
        description="Aspect ratio for the generated image"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Seed for reproducible generation"
    )
    cfg_scale: Optional[float] = Field(
        default=7.0,
        description="Guidance scale for image generation"
    )
    steps: Optional[int] = Field(
        default=30,
        description="Number of diffusion steps"
    )

    @validator('aspect_ratio')
    def validate_aspect_ratio(cls, v):
        """Validate that the aspect ratio is in the expected format."""
        if v not in [e.value for e in AspectRatio]:
            # Still accept custom ratios if they follow the pattern
            if not ((':' in v) or ('.' in v)):
                raise ValueError(f"Invalid aspect ratio format: {v}. Expected format like '16:9' or '2.39:1'")
        return v

    class Config:
        frozen = True


class VideoOutputParams(BaseModel):
    """Parameters for video output."""
    filename: str = Field(
        default="euterpe_output",
        description="Base filename for output without extension"
    )
    duration: Optional[float] = Field(
        default=None,
        description="Duration of the video in seconds"
    )
    fps: Optional[float] = Field(
        default=24.0,
        description="Frames per second"
    )
    resolution: Optional[str] = Field(
        default=None,
        description="Output resolution, e.g., '1920x1080'"
    )
    format: str = Field(
        default="mp4",
        description="Output file format"
    )
    include_audio: bool = Field(
        default=True,
        description="Whether to include audio in the video"
    )

    class Config:
        frozen = True


class Keyframe(BaseModel):
    """A single keyframe for video generation."""
    frame_id: str = Field(
        ..., 
        description="Unique identifier for the keyframe"
    )
    timestamp: float = Field(
        ..., 
        description="Timestamp in seconds where this keyframe appears"
    )
    prompt: str = Field(
        ..., 
        description="Text prompt describing the frame content"
    )
    negative_prompt: Optional[str] = Field(
        default=None,
        description="Elements to exclude from the generated image"
    )
    aspect_ratio: str = Field(
        default=AspectRatio.LANDSCAPE.value,
        description="Aspect ratio for the generated image"
    )
    seed: Optional[int] = Field(
        default=None,
        description="Seed for reproducible generation"
    )
    weight: float = Field(
        default=1.0,
        description="Weight of this keyframe in interpolation"
    )
    image_params: Optional[ImageGenerationParams] = Field(
        default=None,
        description="Specific image generation parameters for this keyframe"
    )

    @validator('timestamp')
    def validate_timestamp(cls, v):
        """Validate that timestamp is not negative."""
        if v < 0:
            raise ValueError(f"Timestamp must be non-negative, got {v}")
        return v

    class Config:
        frozen = True


class EuterpeConfig(BaseModel):
    """Configuration for Euterpe library.
    
    Contains API keys, endpoints and general settings.
    """
    # API keys with defaults from environment variables
    beatoven_api_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("BEATOVEN_API_KEY"),
        description="API key for Beatoven.ai music generation"
    )
    kling_api_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("KLING_API_KEY"),
        description="API key for Kling image generation"
    )
    kling_access_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("KLING_ACCESS_KEY"),
        description="Access key for Kling API (alternative to API key)"
    )
    kling_secret_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("KLING_SECRET_KEY"),
        description="Secret key for Kling API (alternative to API key)"
    )
    dify_api_key: Optional[str] = Field(
        default_factory=lambda: os.environ.get("DIFY_API_KEY"),
        description="API key for Dify prompt enhancement"
    )
    
    # API endpoints
    kling_base_url: Optional[HttpUrl] = Field(
        default_factory=lambda: os.environ.get("KLING_BASE_URL") or "https://api.klingai.com",
        description="Base URL for Kling API"
    )
    beatoven_api_url: Optional[HttpUrl] = Field(
        default_factory=lambda: os.environ.get("BEATOVEN_API_URL") or "https://api.beatoven.ai/v1",
        description="URL for Beatoven API"
    )
    dify_api_url: Optional[HttpUrl] = Field(
        default_factory=lambda: os.environ.get("DIFY_API_URL") or "https://api.dify.ai/v1",
        description="URL for Dify API"
    )
    
    # Output directories
    output_dir: DirectoryPath = Field(
        default="./output",
        description="Base directory for all output files"
    )
    
    # Feature toggles
    use_dify_enhancement: bool = Field(
        default=False,
        description="Whether to use Dify for prompt enhancement"
    )
    
    # Timeouts and retries
    request_timeout: int = Field(
        default=60,
        description="Timeout for API requests in seconds"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for failed requests"
    )

    class Config:
        frozen = True


class VideoGenerationRequest(BaseModel):
    """Request model for video generation."""
    keyframes: List[Keyframe] = Field(
        ..., 
        description="List of keyframes for video generation"
    )
    music_prompt: Optional[str] = Field(
        default=None,
        description="Simple text prompt for music generation"
    )
    music_params: Optional[MusicParams] = Field(
        default=None,
        description="Detailed parameters for music generation"
    )
    output_filename: str = Field(
        default="euterpe_output",
        description="Base filename for output files"
    )
    video_params: Optional[VideoOutputParams] = Field(
        default=None,
        description="Parameters for video output"
    )
    enhance_prompts: bool = Field(
        default=False,
        description="Whether to enhance prompts using Dify"
    )
    enhancement_params: Optional[DifyEnhancementParams] = Field(
        default=None,
        description="Parameters for prompt enhancement"
    )
    default_image_params: Optional[ImageGenerationParams] = Field(
        default=None,
        description="Default parameters for image generation"
    )

    @validator('keyframes')
    def validate_keyframes(cls, v):
        """Validate that keyframes are provided and in chronological order."""
        if not v:
            raise ValueError("At least one keyframe must be provided")
        
        # Ensure keyframes are in order of timestamp
        timestamps = [k.timestamp for k in v]
        if timestamps != sorted(timestamps):
            raise ValueError("Keyframes must be in chronological order by timestamp")
        
        return v

    def get_music_parameters(self) -> MusicParams:
        """Get music parameters, creating from simple prompt if necessary."""
        if self.music_params:
            return self.music_params
        
        if self.music_prompt:
            return MusicParams(prompt=self.music_prompt)
        
        return None

    def get_video_parameters(self) -> VideoOutputParams:
        """Get video parameters, using defaults if necessary."""
        if self.video_params:
            return self.video_params
        
        return VideoOutputParams(filename=self.output_filename)

    class Config:
        frozen = True


class VideoGenerationResult(BaseModel):
    """Result model returned by the generate_video function."""
    success: bool = Field(
        ..., 
        description="Whether the video generation was successful"
    )
    message: str = Field(
        ..., 
        description="Human-readable status message"
    )
    video_filepath: Optional[str] = Field(
        default=None,
        description="Path to the generated video file"
    )
    music_filepath: Optional[str] = Field(
        default=None,
        description="Path to the generated music file"
    )
    image_filepaths: Optional[List[str]] = Field(
        default=None,
        description="Paths to the generated image files"
    )
    error_details: Optional[str] = Field(
        default=None,
        description="Detailed error information if success is False"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the generation process"
    )
    
    class Config:
        frozen = True
