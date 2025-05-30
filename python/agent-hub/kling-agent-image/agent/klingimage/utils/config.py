"""
Configuration utilities for KlingDemo.

This module provides configuration functionality for loading environment variables,
API keys, and other settings needed for the application.
"""
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import os
import time
import jwt
from loguru import logger


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""
    pass


def setup_logging(level: str = "INFO") -> None:
    """
    Set up logging for the application.
    
    Args:
        level: Log level to use (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger.remove()  # Remove default handler
    logger.add(
        "klingdemo.log", 
        level=level, 
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        retention="1 week"
    )
    # Also add stderr output
    logger.add(
        lambda msg: print(msg, end=""),
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )


def generate_jwt_token(access_key: str, secret_key: str, expiration_seconds: int = 1800) -> str:
    """
    Generate a JWT token for API authentication.
    
    Args:
        access_key: The API access key (ak)
        secret_key: The API secret key (sk)
        expiration_seconds: Token validity period in seconds (default: 30 minutes)
        
    Returns:
        JWT token as a string
    """
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # Set up payload
    current_time = int(time.time())
    payload = {
        "iss": access_key,
        "exp": current_time + expiration_seconds,
        "nbf": current_time - 5  # Allow for slight clock skew
    }
    
    # Generate token
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)
    
    return token


def load_config(env_file: Optional[str] = None) -> dict:
    """
    Load configuration from environment variables or .env file.
    
    Args:
        env_file: Path to .env file (optional)
        
    Returns:
        Dict containing configuration values
        
    Raises:
        ConfigurationError: If required environment variables are missing
    """
    # If env_file is provided, load it
    if env_file and Path(env_file).exists():
        load_dotenv(env_file)
    else:
        # Try to find .env in current directory or parent
        env_paths = ['.env', '../.env', '../../.env']
        for path in env_paths:
            if Path(path).exists():
                load_dotenv(path)
                break
    
    # Get API credentials from environment
    access_key = os.getenv('ACCESSKEY_API')
    secret_key = os.getenv('ACCESSKEY_SECRET')
    
    if not access_key:
        raise ConfigurationError("ACCESSKEY_API environment variable is required")
    if not secret_key:
        raise ConfigurationError("ACCESSKEY_SECRET environment variable is required")
    
    # Get API base URL (or use default)
    api_base_url = os.getenv('KLING_API_BASE_URL', 'https://api.klingai.com')
    
    # Generate JWT token for authentication
    token_expiration = int(os.getenv('KLING_TOKEN_EXPIRATION', '1800'))  # Default: 30 minutes
    jwt_token = generate_jwt_token(access_key, secret_key, token_expiration)
    
    return {
        'access_key': access_key,
        'secret_key': secret_key,
        'jwt_token': jwt_token,
        'token_expiration': token_expiration,
        'api_base_url': api_base_url,
        'timeout': int(os.getenv('KLING_API_TIMEOUT', '60')),  # Default timeout: 60 seconds
        'max_retries': int(os.getenv('KLING_API_MAX_RETRIES', '3')),  # Default max retries: 3
    }