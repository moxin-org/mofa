"""Euterpe - A Python library for AI-driven music and video generation.

This package provides tools for generating music and videos using AI services.
"""

# Re-export key classes from the internal package
from .euterpe.models import AspectRatio, MusicParams, ImageModel
from .euterpe.api import generate_video

# Version information
__version__ = "0.1.0"
