"""
Client module for interacting with the Beatoven.ai API.
"""
import asyncio
from pathlib import Path
import os
import logging
from typing import Any, Dict, Optional, Union

from .models import TaskResponse, TextPrompt, TrackRequest, TrackStatus
from .config import get_settings, settings

# Setup logger
logger = logging.getLogger("beatoven_ai")


class BeatovenAIError(Exception):
    """Base exception for Beatoven.ai API errors."""
    pass


class BeatovenClient:
    """
    Client for interfacing with the Beatoven.ai API.
    Provides methods for generating music based on text prompts.
    """

    def __init__(self, api_key: Optional[str] = None, env_file: Optional[Union[str, Path]] = None):
        """
        Initialize the Beatoven.ai client.
        
        Args:
            api_key: Optional API key. If not provided, will use the one from settings.
            env_file: Optional path to a custom .env file. If provided, will load settings from this file.
        """
        # Load custom settings if env_file is provided, otherwise use the global settings
        self.settings = get_settings(env_file) if env_file else settings
        
        # Use the provided API key or the one from settings
        self.api_key = api_key or self.settings.API_KEY
        self.api_url = self.settings.API_URL
        
        if not self.api_key:
            logger.warning("No Beatoven.ai API key provided. Music generation will not function.")
    
    async def compose_track(self, request: TrackRequest) -> TaskResponse:
        """
        Start a track composition task.
        
        Args:
            request: Track request with prompt and optional parameters.
            
        Returns:
            TaskResponse: Response containing the task ID.
            
        Raises:
            BeatovenAIError: If the API request fails.
        """
        if not self.api_key:
            raise BeatovenAIError("API key is required for music generation")
            
        # Mock implementation for simplified integration
        logger.info(f"Simulating music generation with prompt: {request.prompt.text}")
        await asyncio.sleep(1)  # Simulate API call delay
        
        # Return a mock task ID
        task_id = f"mock-ta***REMOVED***{id(request)}"
        return TaskResponse(task_id=task_id)
    
    async def check_status(self, task_id: str) -> TrackStatus:
        """
        Check the status of a composition task.
        
        Args:
            task_id: The ID of the task to check.
            
        Returns:
            TrackStatus: Current status of the track.
            
        Raises:
            BeatovenAIError: If the API request fails.
        """
        if not self.api_key:
            raise BeatovenAIError("API key is required to check task status")
            
        # Mock implementation for simplified integration
        logger.info(f"Checking status for task: {task_id}")
        await asyncio.sleep(0.5)  # Simulate API call delay
        
        # Return a mock completion status
        return TrackStatus(
            status="completed", 
            meta={"track_url": f"https://example.com/{task_id}.mp3"}
        )
    
    async def download_track(self, track_url: str, output_path: Optional[Union[str, Path]] = None) -> Path:
        """
        Download a generated track to a local file.
        
        Args:
            track_url: URL of the track to download.
            output_path: Optional custom output path. If not provided, will use the default directory.
            
        Returns:
            Path: Path to the downloaded file.
            
        Raises:
            BeatovenAIError: If the download fails.
        """
        if not self.api_key:
            raise BeatovenAIError("API key is required to download tracks")
            
        # Determine output path
        if not output_path:
            dir_path = Path(self.settings.OUTPUT_DIR)
            dir_path.mkdir(exist_ok=True, parents=True)
            file_name = Path(track_url).name
            output_path = dir_path / file_name
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Mock downloading the file
        logger.info(f"Simulating download of track from {track_url} to {output_path}")
        await asyncio.sleep(1)  # Simulate download delay
        
        # Create an empty file to simulate the download
        with open(output_path, 'wb') as f:
            f.write(b'mock audio data')
            
        return output_path
    
    async def generate_and_wait(
        self,
        prompt: Union[str, TextPrompt],
        format: str = "mp3",
        duration: int = 180,
        output_path: Optional[Union[str, Path]] = None,
        timeout: float = 60.0
    ) -> Path:
        """
        Generate a track from a prompt and wait for completion.
        
        This is a convenience method that handles the full workflow:
        1. Submit a track request
        2. Poll for completion
        3. Download the track when ready
        
        Args:
            prompt: Text prompt or TextPrompt object.
            format: Audio format ("mp3", "wav", "ogg").
            duration: Duration in seconds (30-600).
            output_path: Optional custom output path.
            timeout: Maximum time to wait for completion in seconds.
            
        Returns:
            Path: Path to the downloaded track file.
            
        Raises:
            BeatovenAIError: If any step in the process fails.
            TimeoutError: If the track generation exceeds the timeout.
        """
        # Handle string or TextPrompt
        if isinstance(prompt, str):
            prompt = TextPrompt(text=prompt)
            
        # Create track request
        request = TrackRequest(
            prompt=prompt,
            format=format,
            duration=duration
        )
        
        # Start composition
        logger.info(f"Starting track generation with prompt: {prompt.text}")
        task_response = await self.compose_track(request)
        task_id = task_response.task_id
        
        # Poll for completion
        start_time = asyncio.get_event_loop().time()
        while True:
            # Check for timeout
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise TimeoutError(f"Track generation timed out after {timeout} seconds")
                
            # Check status
            status = await self.check_status(task_id)
            
            if status.status == "completed":
                if status.meta and "track_url" in status.meta:
                    # Download the track
                    return await self.download_track(status.meta["track_url"], output_path)
                else:
                    raise BeatovenAIError("Track completed but no download URL provided")
                    
            elif status.status == "failed":
                raise BeatovenAIError("Track generation failed")
                
            # Wait before polling again
            await asyncio.sleep(2)
