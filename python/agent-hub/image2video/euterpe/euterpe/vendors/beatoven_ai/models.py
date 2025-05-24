"""
Models for beatoven_ai integration in Euterpe.
"""
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class TextPrompt(BaseModel):
    """Text prompt model for music generation."""
    text: str = Field(..., description="Text description for music generation")


class TrackRequest(BaseModel):
    """Model representing a track generation request."""
    prompt: TextPrompt
    format: Literal["mp3", "wav", "ogg"] = Field(default="mp3", description="Audio format")
    duration: int = Field(default=180, description="Duration in seconds", ge=30, le=600)


class TaskResponse(BaseModel):
    """Model representing the response from the composition API."""
    task_id: str = Field(..., description="ID of the composition task")


class TrackStatus(BaseModel):
    """Model representing the status of a track generation task."""
    status: Literal["composing", "composed", "completed", "failed"] = Field(..., description="Current status of the task")
    meta: Optional[Dict[str, Any]] = Field(None, description="Additional metadata, including track_url when completed")
