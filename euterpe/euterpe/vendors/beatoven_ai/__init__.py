"""Beatoven AI vendor module integrated into Euterpe.

This module contains the core functionality from the BeatovenDemo package
integrated directly into Euterpe for simplified usage.
"""

from euterpe.vendors.beatoven_ai.client import BeatovenClient, BeatovenAIError
from euterpe.vendors.beatoven_ai.models import TrackRequest, TextPrompt, TaskResponse, TrackStatus
from euterpe.vendors.beatoven_ai.config import Settings, get_settings

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
