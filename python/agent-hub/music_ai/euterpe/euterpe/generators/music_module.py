"""Music generation module for the Euterpe library.

This module interfaces with the BeatovenDemo library for music generation.
"""

import asyncio
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Optional, Dict, Any, Union

from pydantic import BaseModel, Field

# Set up logger
logger = logging.getLogger(__name__)

# Import BeatovenDemo components from our vendors package
from ..vendors.beatoven_ai.client import BeatovenClient
from ..vendors.beatoven_ai.models import TrackRequest, TextPrompt
from ..vendors.beatoven_ai.config import get_settings, Settings
BEATOVEN_AVAILABLE = True


class MusicGeneratorConfig(BaseModel):
    """Configuration for the music generator."""
    api_key: Optional[str] = None
    api_url: Optional[str] = Field(default="https://api.beatoven.ai/v1")
    timeout: int = 300
    output_dir: Path = Field(default=Path("./output/music"))
    default_duration: int = 180
    default_format: str = "mp3"
    mock_mode: bool = Field(default=False, description="Use mock implementation instead of real API calls")
    
    class Config:
        validate_assignment = True


class MusicGenerator:
    """Generate music using the BeatovenDemo library."""
    
    def __init__(self, config: MusicGeneratorConfig):
        """Initialize the music generator.
        
        Args:
            config: Configuration for the music generator.
        """
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Beatoven client if available
        self.client = None
        self.settings = None
        
        if BEATOVEN_AVAILABLE and not self.config.mock_mode:
            try:
                # Create settings without loading from env file
                self.settings = get_settings(None)
                
                # Override settings with our configuration
                self.settings.API_KEY = self.config.api_key
                self.settings.API_URL = self.config.api_url
                self.settings.DEFAULT_DURATION = self.config.default_duration
                self.settings.DEFAULT_FORMAT = self.config.default_format
                self.settings.OUTPUT_DIR = str(self.config.output_dir)
                
                # Initialize client with our settings
                self.client = BeatovenClient(api_key=self.settings.API_KEY)
                logger.info("Initialized Beatoven client for music generation")
                
            except Exception as e:
                logger.error(f"Failed to initialize Beatoven client: {e}")
                logger.warning("Falling back to mock implementation")
                self.config.mock_mode = True
        else:
            logger.warning("BeatovenDemo library not available or mock mode enabled")
            self.config.mock_mode = True
        
    async def generate(
        self,
        prompt: str,
        duration: Optional[float] = None,
        genre: Optional[str] = None,
        tempo: Optional[int] = None,
        format: Optional[str] = None,
        filename: str = "music_output",
    ) -> Optional[Path]:
        """Generate music using the BeatovenDemo library.
        
        Args:
            prompt: Text prompt describing the music.
            duration: Optional duration in seconds.
            genre: Optional music genre.
            tempo: Optional tempo in beats per minute.
            format: Output audio format (mp3, wav, ogg).
            filename: Output file name without extension.
            
        Returns:
            Path: Path to the generated music file, or None if generation failed.
            
        Raises:
            Exception: If music generation fails.
        """
        try:
            # Use defaults from config if parameters not provided
            if duration is None:
                duration = self.config.default_duration
            if format is None:
                format = self.config.default_format
                
            # Enhance prompt with genre and tempo if provided
            enhanced_prompt = prompt
            if genre:
                enhanced_prompt += f", genre: {genre}"
            if tempo:
                enhanced_prompt += f", tempo: {tempo} bpm"
                
            logger.info(f"Generating music with prompt: {enhanced_prompt[:50]}...")
            
            if self.config.mock_mode:
                # Mock implementation
                logger.info(f"[MOCK MODE] Generating music for prompt: {enhanced_prompt[:30]}...")
                
                # Simulate API delay based on duration
                await asyncio.sleep(min(3, duration / 60))  # Shorter delay for testing
                
                # Create a simple mock audio file using a system sound or silence
                try:
                    import numpy as np
                    from scipy.io import wavfile
                    
                    # Generate a simple sine wave as mock audio
                    sample_rate = 44100
                    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
                    
                    # Create a simple melody based on the hash of the prompt
                    import hashlib
                    prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest(), 16)
                    
                    # Use hash to determine frequency and modulation
                    base_freq = 220 + (prompt_hash % 440)  # A3 to A4 range
                    mod_freq = 0.25 + (prompt_hash % 100) / 100  # Modulation frequency
                    
                    # Generate a melodic pattern
                    audio = 0.5 * np.sin(2 * np.pi * base_freq * t)
                    audio += 0.3 * np.sin(2 * np.pi * (base_freq * 1.5) * t)  # Fifth
                    audio += 0.2 * np.sin(2 * np.pi * (base_freq * 2) * t)    # Octave
                    
                    # Add amplitude modulation
                    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * mod_freq * t)
                    audio = audio * envelope
                    
                    # Ensure audio is in the range [-1, 1]
                    audio = np.clip(audio, -1, 1)
                    
                    # Convert to int16 format
                    audio_int16 = (audio * 32767).astype(np.int16)
                    
                    # Save as WAV first
                    temp_wav_path = self.config.output_dir / f"{filename}_temp.wav"
                    wavfile.write(temp_wav_path, sample_rate, audio_int16)
                    
                    # Convert to requested format if not WAV
                    output_path = self.config.output_dir / f"{filename}.{format}"
                    if format.lower() == "wav":
                        # Just copy the WAV file
                        import shutil
                        shutil.copy(temp_wav_path, output_path)
                    else:
                        # Convert using ffmpeg if available
                        try:
                            import ffmpeg
                            ffmpeg.input(str(temp_wav_path)).output(str(output_path)).run(quiet=True, overwrite_output=True)
                        except Exception:
                            # Fall back to just using the WAV file with renamed extension
                            shutil.copy(temp_wav_path, output_path)
                    
                    # Clean up temp file
                    if temp_wav_path.exists():
                        os.remove(temp_wav_path)
                    
                except ImportError:
                    # If numpy/scipy not available, create an empty file
                    output_path = self.config.output_dir / f"{filename}.{format}"
                    with open(output_path, 'wb') as f:
                        f.write(b'MOCK AUDIO FILE')
                
                logger.info(f"[MOCK MODE] Generated mock audio at {output_path}")
                return output_path
                
            else:
                # Real implementation using Beatoven client
                output_path = await self.client.generate_music(
                    prompt=enhanced_prompt,
                    duration=int(duration),  # Beatoven expects int
                    format=format,
                    output_path=str(self.config.output_dir),
                    filename=filename
                )
                
                logger.info(f"Music generated at: {output_path}")
                return Path(output_path)
                
        except Exception as e:
            logger.error(f"Error generating music: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
            
    async def create_track_from_text(self, prompt: str, duration: Optional[int] = None, 
                                   format: Optional[str] = None) -> Dict[str, Any]:
        """Create a track from a text prompt using the low-level Beatoven API.
        
        This is a more direct method that exposes the underlying API functionality.
        
        Args:
            prompt: Text prompt describing the music.
            duration: Music duration in seconds.
            format: Output audio format.
            
        Returns:
            Dict containing track status information.
        """
        if self.config.mock_mode:
            logger.warning("create_track_from_text not supported in mock mode")
            return {"mock": True, "status": "completed", "track_id": "mock_track_id"}
            
        # Use defaults if not specified
        if duration is None:
            duration = self.config.default_duration
        if format is None:
            format = self.config.default_format
            
        # Create track request
        track_request = TrackRequest(
            prompt=TextPrompt(text=prompt),
            duration=duration,
            format=format
        )
        
        async with aiohttp.ClientSession() as session:
            # Start composition
            compose_response = await self.client.compose_track(session, track_request)
            task_id = compose_response.task_id
            logger.info(f"Composition started with task ID: {task_id}")
            
            # Wait for completion
            track_status = await self.client.watch_task_status(session, task_id)
            return track_status.dict()
