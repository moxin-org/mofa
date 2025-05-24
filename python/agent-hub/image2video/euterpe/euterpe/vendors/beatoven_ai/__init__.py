"""Beatoven AI vendor module integrated into Euterpe.

This module contains the core functionality from the BeatovenDemo package
integrated directly into Euterpe for simplified usage.
"""

from .client import BeatovenClient, BeatovenAIError
from .models import TrackRequest, TextPrompt, TaskResponse, TrackStatus
from .config import Settings, get_settings

__all__ = [
    "BeatovenClient", 
    "BeatovenAIError", 
    "TrackRequest", 
    "TextPrompt",
    "TaskResponse",
    "TrackStatus",
    "Settings",
    "get_settings"
]
