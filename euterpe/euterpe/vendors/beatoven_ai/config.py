"""
Configuration module with environment variable support for Beatoven AI integration.
"""
from functools import lru_cache
from pathlib import Path
from typing import Optional, Union
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    """Application settings that can be loaded from environment variables."""
    
    # API configuration
    API_URL: str = Field(
        default="https://public-api.beatoven.ai/api/v1",
        description="Beatoven.ai API URL"
    )
    API_KEY: str = Field(
        default="",
        description="Beatoven.ai API key"
    )
    
    # Default music generation settings
    DEFAULT_DURATION: int = Field(
        default=180,
        description="Default music duration in seconds",
        ge=30,
        le=600
    )
    DEFAULT_FORMAT: str = Field(
        default="mp3",
        description="Default audio format (mp3, wav, ogg)"
    )
    
    # Output directory
    OUTPUT_DIR: str = Field(
        default="./",
        description="Directory to save generated music files"
    )


@lru_cache
def get_settings(env_file: Optional[Union[str, Path]] = None) -> Settings:
    """
    Create and return a cached Settings instance.
    
    Args:
        env_file: Optional path to an environment file.
        
    Returns:
        Settings: Application settings.
    """
    environment = {}
    
    # Load from env file if provided
    if env_file:
        env_path = Path(env_file)
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        environment[key.strip()] = value.strip().strip('"').strip("'")
    
    # Initialize settings with env values
    settings_kwargs = {}
    for field_name, field in Settings.__fields__.items():
        env_val = environment.get(field_name) or os.environ.get(field_name)
        if env_val is not None:
            settings_kwargs[field_name] = env_val
            
    return Settings(**settings_kwargs)


# Global settings instance
settings = get_settings()
