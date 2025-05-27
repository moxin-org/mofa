"""Dify API client for text prompt enhancement.

This module provides a client to enhance text prompts using the Dify API.
"""

import asyncio
import logging
import os
from typing import Optional, Dict, Any, List, Union

import requests
from pydantic import BaseModel, HttpUrl, Field

# Set up logger
logger = logging.getLogger(__name__)


class DifyEnhancerConfig(BaseModel):
    """Configuration for the Dify enhancer client."""
    api_key: Optional[str] = None
    api_url: HttpUrl = Field(default="https://api.dify.ai/v1")
    timeout: int = 60
    enhancement_level: str = Field(default="standard")  # minimal, standard, detailed
    mock_mode: bool = Field(default=False)

    class Config:
        validate_assignment = True


class DifyProcessingError(Exception):
    """Exception raised when Dify processing fails."""
    pass


class DifyClient:
    """Client for the Dify API to enhance text prompts."""
    
    def __init__(self, config: Optional[DifyEnhancerConfig] = None):
        """Initialize the Dify client.
        
        Args:
            config: Optional configuration. If not provided, will try to load from environment.
        """
        if config is None:
            api_key = os.environ.get("DIFY_API_KEY")
            api_url = os.environ.get("DIFY_API_URL", "https://api.dify.ai/v1")
            
            if not api_key:
                logger.warning("DIFY_API_KEY environment variable not set. Using mock mode.")
                config = DifyEnhancerConfig(mock_mode=True)
            else:
                config = DifyEnhancerConfig(api_key=api_key, api_url=api_url)
            
        self.config = config
        
        # Initialize headers if we have an API key
        self.headers = None
        if self.config.api_key:
            self.headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json"
            }
            logger.info(f"Initialized Dify client with API URL: {self.config.api_url}")
        else:
            logger.warning("Dify client initialized in mock mode - no API key provided")
            self.config.mock_mode = True
    
    def enhance_prompt(
        self, 
        prompt: str, 
        context_keywords: Optional[List[str]] = None,
        enhancement_level: Optional[str] = None
    ) -> str:
        """Enhance a text prompt using Dify API.
        
        Args:
            prompt: The original text prompt to enhance.
            context_keywords: Optional list of keywords to provide context.
            enhancement_level: Level of enhancement (minimal, standard, detailed).
                If not provided, uses the config default.
            
        Returns:
            str: The enhanced prompt text.
            
        Raises:
            DifyProcessingError: If the API call fails.
        """
        if not prompt:
            logger.warning("Empty prompt provided for enhancement")
            return prompt
            
        try:
            enhancement_level = enhancement_level or self.config.enhancement_level
            logger.info(f"Enhancing prompt with level '{enhancement_level}': {prompt[:50]}...")
            
            if self.config.mock_mode:
                # Mock implementation
                logger.info("[MOCK MODE] Using mock enhancement")
                
                # Simulate enhancement based on level
                if enhancement_level == "minimal":
                    enhanced = f"{prompt}, high quality, detailed"
                elif enhancement_level == "standard":
                    enhanced = f"{prompt}, high quality, detailed, professional lighting, sharp focus"
                else:  # detailed
                    enhanced = (f"{prompt}, high quality, detailed, professional lighting, "
                               f"sharp focus, high resolution, realistic texture, vivid colors")
                
                # Add context keywords if provided
                if context_keywords:
                    context_str = ", ".join(context_keywords)
                    enhanced = f"{enhanced}, {context_str}"
                
                logger.info(f"[MOCK MODE] Enhanced prompt: {enhanced[:50]}...")
                return enhanced
                
            else:
                # Real implementation
                if not self.headers:
                    raise DifyProcessingError("Dify API key not configured")
                
                # Build context string if keywords provided
                context = ""
                if context_keywords:
                    context = f"Context keywords: {', '.join(context_keywords)}"
                
                # Prepare inputs based on enhancement level
                inputs = {
                    "text": prompt,
                    "enhancement_level": enhancement_level
                }
                
                if context:
                    inputs["context"] = context
                
                payload = {
                    "inputs": inputs,
                    "response_mode": "blocking"
                }
                
                # Make API call
                response = requests.post(
                    f"{self.config.api_url}/workflows/run", 
                    headers=self.headers,
                    json=payload,
                    timeout=self.config.timeout
                )
                
                if response.status_code != 200:
                    error_msg = f"Dify API returned status {response.status_code}"
                    try:
                        error_data = response.json()
                        if "error" in error_data:
                            error_msg += f": {error_data['error']}"
                    except Exception:
                        error_msg += f": {response.text[:100]}"
                        
                    raise DifyProcessingError(error_msg)
                
                # Parse response
                result = response.json()
                
                # Extract enhanced prompt from the response
                enhanced_prompt = None
                
                if "output" in result and isinstance(result["output"], dict):
                    # Check for common response formats
                    if "enhanced_prompt" in result["output"]:
                        enhanced_prompt = result["output"]["enhanced_prompt"]
                    elif "text" in result["output"]:
                        enhanced_prompt = result["output"]["text"]
                    elif "result" in result["output"]:
                        enhanced_prompt = result["output"]["result"]
                
                if enhanced_prompt is None:
                    logger.warning(f"Could not extract enhanced prompt from response: {result}")
                    return prompt  # Return the original prompt if extraction fails
                
                logger.info(f"Prompt enhanced successfully: {enhanced_prompt[:50]}...")
                return enhanced_prompt
                
        except DifyProcessingError as e:
            # Re-raise specific Dify errors
            raise
        except Exception as e:
            # Log and re-raise other exceptions
            logger.error(f"Error enhancing prompt: {type(e).__name__}: {e}")
            raise DifyProcessingError(f"Failed to enhance prompt: {str(e)}")
    
    async def enhance_prompts_batch(
        self, 
        prompts: List[str],
        context_keywords: Optional[List[str]] = None,
        enhancement_level: Optional[str] = None
    ) -> List[str]:
        """Enhance multiple prompts in parallel.
        
        Args:
            prompts: List of prompts to enhance.
            context_keywords: Optional list of keywords to provide context.
            enhancement_level: Level of enhancement.
            
        Returns:
            List[str]: List of enhanced prompts.
        """
        if not prompts:
            return []
            
        # Create a task for each prompt enhancement
        async def enhance_single(prompt):
            # Run the synchronous method in an executor
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                lambda: self.enhance_prompt(
                    prompt, context_keywords, enhancement_level
                )
            )
        
        # Process all prompts in parallel
        tasks = [enhance_single(p) for p in prompts]
        return await asyncio.gather(*tasks)
