"""
Configuration handling for the workflow.
"""
import os
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Import the Pydantic settings from BeatovenDemo
from beatoven_ai.beatoven_ai.config import get_settings

logger = logging.getLogger(__name__)

def setup_logging(level=logging.INFO):
    """Set up basic logging configuration."""
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env_file(env_file: Optional[str]) -> Dict[str, str]:
    """
    Load environment variables from a .env file without affecting system environment.
    
    Args:
        env_file: Path to the .env file
        
    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    if (env_file and Path(env_file).exists()):
        try:
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = line.split('=', 1)
                    env_vars[key] = value
            logger.info(f"Loaded environment variables from {env_file}")
        except Exception as e:
            logger.error(f"Failed to parse env file {env_file}: {e}")
    return env_vars

def load_kling_config(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load KlingDemo configuration from .env file or environment variables.
    
    Args:
        env_file: Path to the .env file
        
    Returns:
        Dictionary with KlingDemo configuration
    """
    # First try to load from specific env file
    env_vars = load_env_file(env_file)
    
    # Configuration with priorities: env_file, then system env vars
    config = {
        'access_key': env_vars.get('ACCESSKEY_API') or os.environ.get('ACCESSKEY_API'),
        'secret_key': env_vars.get('ACCESSKEY_SECRET') or os.environ.get('ACCESSKEY_SECRET'),
        'api_base_url': env_vars.get('KLING_API_BASE_URL') or os.environ.get('KLING_API_BASE_URL', 'https://api.klingai.com'),
        'timeout': int(env_vars.get('KLING_TIMEOUT') or os.environ.get('KLING_TIMEOUT', '60')),
        'max_retries': int(env_vars.get('KLING_MAX_RETRIES') or os.environ.get('KLING_MAX_RETRIES', '3'))
    }
    
    # Validate required fields
    if not config['access_key'] or not config['secret_key']:
        raise ValueError("Missing required KlingDemo API credentials. Set KLING_ACCESS_KEY and KLING_SECRET_KEY in environment or .env file.")
    
    return config

def load_beatoven_config(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load BeatovenDemo configuration using the Pydantic settings system.

    Args:
        env_file: Path to the .env file

    Returns:
        Dictionary with BeatovenDemo configuration from the settings
    """
    # Import the get_settings function
    from beatoven_ai import get_settings

    try:
        # Check if the env_file exists before attempting to use it
        if env_file and Path(env_file).exists():
            logger.info(f"Loading BeatovenDemo configuration from {env_file}")
            # Use the provided env file path
            custom_settings = get_settings(env_file)
        else:
            if env_file:
                logger.warning(f"BeatovenDemo environment file {env_file} not found, using default settings")
            else:
                logger.info("Using default BeatovenDemo settings (no env file specified)")

            # Create a settings instance without any env file
            custom_settings = get_settings(None)

        # Return a dictionary representation of the settings
        config = {
            'api_key': custom_settings.API_KEY,
            'api_url': custom_settings.API_URL,
            'default_duration': custom_settings.DEFAULT_DURATION,
            'default_format': custom_settings.DEFAULT_FORMAT,
            'output_dir': custom_settings.OUTPUT_DIR,
            'request_timeout': custom_settings.REQUEST_TIMEOUT,
            'download_timeout': custom_settings.DOWNLOAD_TIMEOUT,
            'polling_interval': custom_settings.POLLING_INTERVAL
        }

        # Mask API key for logging
        if config['api_key']:
            masked_key = f"{config['api_key'][:4]}...{config['api_key'][-4:]}" if len(config['api_key']) > 8 else "****"
            logger.info(f"Loaded BeatovenDemo API key: {masked_key}")
        else:
            logger.warning("BeatovenDemo API key not found. Music generation will not be available.")

        logger.info(f"Using BeatovenDemo API URL: {config['api_url']}")

        return config

    except Exception as e:
        logger.error(f"Failed to load BeatovenDemo configuration: {e}")
        # Return a minimal configuration that will allow the application to continue
        return {
            'api_key': '',
            'api_url': 'https://public-api.beatoven.ai/api/v1',
            'default_duration': 180,
            'default_format': 'mp3',
            'output_dir': './outputs',
            'request_timeout': 30,
            'download_timeout': 60,
            'polling_interval': 10
        }
def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run an integrated workflow with KlingDemo, BeatovenDemo, and optional Dify")
    
    parser.add_argument(
        "--keyframes-file",
        type=Path,
        default=Path("workflow/keyframes.txt"),
        help="Path to the keyframes file"
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("workflow/outputs"),
        help="Directory to save output files"
    )
    
    parser.add_argument(
        "--model-name",
        type=str,
        default="kling-v1-5",
        help="Model name for image generation"
    )
    
    parser.add_argument(
        "--env-file",
        type=str,
        default=None,
        help="Path to .env file with KlingDemo API credentials"
    )
    
    parser.add_argument(
        "--beatoven-env-file",
        type=str,
        default=".env.beatoven",
        help="Path to .env file with BeatovenDemo API credentials"
    )
    
    parser.add_argument(
        "--use-dify",
        action="store_true",
        help="Use Dify to enhance prompts for video generation"
    )
    
    parser.add_argument(
        "--music-prompt",
        type=str,
        default=None,
        help="Prompt for generating background music for the entire workflow"
    )
    
    parser.add_argument(
        "--music-filename",
        type=str,
        default="piano_meditation",
        help="Filename for the generated music file (without extension)"
    )
    
    return parser.parse_args()