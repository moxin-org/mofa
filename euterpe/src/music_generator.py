"""
Music generation module using the Beatoven.ai API.
"""
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Import BeatovenDemo with its settings capabilities
import sys
import aiohttp
import beatoven_ai
from beatoven_ai.beatoven_ai.config import get_settings, Settings
from beatoven_ai import BeatovenClient

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

logger = logging.getLogger(__name__)

class MusicGenerator:
    """Handles music generation using BeatovenDemo."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None, output_dir: Optional[Path] = None, env_file: Optional[str] = None):
        """
        Initialize the music generator with API credentials.

        Args:
            api_key: Beatoven API key (overrides env_file settings)
            api_url: Beatoven API URL (overrides env_file settings)
            output_dir: Directory to save generated music files (overrides env_file settings)
            env_file: Path to environment file for settings
        """
        # Load settings from env_file if provided
        if env_file and Path(env_file).exists():
            logger.info(f"Loading music generator settings from {env_file}")
            self.settings = get_settings(env_file)
        else:
            # Use an empty settings object without loading any env file
            self.settings = get_settings(None)

            # Override settings with explicit parameters if provided
        if api_key:
            self.settings.API_KEY = api_key
        if api_url:
            self.settings.API_URL = api_url
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            self.settings.OUTPUT_DIR = str(output_dir)

        # Initialize client with our settings and explicitly pass the same env_file
        # This ensures the client uses the same configuration without searching for other .env files
        self.client = BeatovenClient(
            api_key=self.settings.API_KEY,
            env_file=env_file
        )

        logger.info("Initialized music generator with Beatoven settings")
    async def generate(self, prompt: str, duration: int = None, 
                      format: str = None, filename: str = "background_music") -> Optional[Path]:
        """
        Generate music based on a text prompt.
        
        Args:
            prompt: Text prompt describing the desired music
            duration: Music duration in seconds (uses DEFAULT_DURATION from settings if None)
            format: Output audio format (mp3, wav, ogg) (uses DEFAULT_FORMAT from settings if None)
            filename: Output filename (without extension)
            
        Returns:
            Path to the generated audio file, or None if generation failed
        """
        if not self.settings.API_KEY:
            logger.warning("Cannot generate music: Beatoven API key is not configured")
            return None
        
        # Use settings defaults if parameters not provided
        if duration is None:
            duration = self.settings.DEFAULT_DURATION
        if format is None:
            format = self.settings.DEFAULT_FORMAT
            
        try:
            logger.info(f"Generating music with prompt: {prompt[:50]}...")
            
            # Create output directory if it doesn't exist
            output_dir = Path(self.settings.OUTPUT_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Use the client's generate_music method which handles the session internally
            output_path = await self.client.generate_music(
                prompt=prompt,
                duration=duration,
                format=format,
                output_path=str(output_dir),
                filename=filename
            )
            
            logger.info(f"Music generated at: {output_path}")
            return Path(output_path)
            
        except Exception as e:
            logger.error(f"Failed to generate music: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
            
    async def create_track_from_text(self, prompt: str, duration: int = None, audio_format: str = None):
        """
        Create a track from a text prompt using the BeatovenClient.
        
        This method directly uses the BeatovenClient's methods that require a session.
        
        Args:
            prompt: Text prompt describing the desired music
            duration: Music duration in seconds
            audio_format: Output audio format (mp3, wav, ogg)
            
        Returns:
            TrackStatus object with track details
        """
        # Use settings defaults if parameters not provided
        if duration is None:
            duration = self.settings.DEFAULT_DURATION
        if audio_format is None:
            audio_format = self.settings.DEFAULT_FORMAT
            
        from beatoven_ai.beatoven_ai.models import TrackRequest, TextPrompt
        
        track_request = TrackRequest(
            prompt=TextPrompt(text=prompt),
            duration=duration,
            format=audio_format
        )
        
        async with aiohttp.ClientSession() as session:
            # Step 1: Start composition
            compose_response = await self.client.compose_track(session, track_request)
            task_id = compose_response.task_id
            logger.info(f"Composition started with task ID: {task_id}")
            
            # Step 2: Wait for completion
            track_status = await self.client.watch_task_status(session, task_id)
            
            return track_status
            
    async def download_track(self, track_id: str, output_path: str, timeout: int = None):
        """
        Download a track using the track ID.
        
        Args:
            track_id: ID of the track to download
            output_path: Path where the file should be saved
            timeout: Download timeout in seconds
            
        Returns:
            Path to the downloaded file
        """
        async with aiohttp.ClientSession() as session:
            # First get the track status to get the download URL
            track_status = await self.client.get_track_status(session, track_id)
            
            if track_status.status != "completed" or not track_status.meta or "track_url" not in track_status.meta:
                raise ValueError(f"Track {track_id} is not available for download")
                
            track_url = track_status.meta["track_url"]
            
            # Set timeout from settings if not provided
            if timeout is None:
                timeout = self.settings.DOWNLOAD_TIMEOUT
                
            # Extract filename and format from output_path
            output_path_obj = Path(output_path)
            filename = output_path_obj.stem
            format = output_path_obj.suffix.lstrip('.')
            
            # Download the file
            return await self.client.handle_track_file(
                session,
                track_url,
                output_path=str(output_path_obj.parent),
                filename=filename,
                format=format
            )