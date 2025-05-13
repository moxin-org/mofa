"""
Dify integration module for enhancing prompts.
"""
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

class DifyProcessingError(Exception):
    """Exception raised when Dify processing fails."""
    pass

class DifyEnhancer:
    """Handles prompt enhancement using Dify integration."""
    
    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize the Dify enhancer.
        
        Args:
            api_key: Dify API key
            api_url: Dify API URL
        """
        self.api_key = api_key
        self.api_url = api_url or "https://api.dify.ai/v1"
        logger.info("Initialized Dify enhancer")
    
    def enhance_prompt(self, prompt: str) -> str:
        """
        Enhance a prompt using Dify's workflow.
        
        Args:
            prompt: The original prompt to enhance
            
        Returns:
            Enhanced prompt
            
        Raises:
            DifyProcessingError: If the Dify API call fails
        """
        try:
            logger.info(f"Enhancing prompt with Dify: {prompt[:50]}...")
            
            # Import from examples or use direct API call
            try:
                import sys
                import os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'examples'))
                from external_dify_demo import call_dify_workflow
                
                enhanced_prompt = call_dify_workflow(prompt)
                
            except ImportError:
                # Fallback to direct API implementation if the import fails
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "inputs": {
                        "text": prompt
                    },
                    "response_mode": "blocking"
                }
                
                response = requests.post(
                    f"{self.api_url}/workflows/run", 
                    headers=headers, 
                    json=payload
                )
                
                if response.status_code != 200:
                    raise DifyProcessingError(f"Dify API returned status {response.status_code}: {response.text}")
                
                result = response.json()
                if "error" in result:
                    raise DifyProcessingError(f"Dify processing error: {result['error']}")
                
                enhanced_prompt = result.get("output", {}).get("enhanced_prompt", prompt)
            
            logger.info(f"Prompt enhanced: {enhanced_prompt[:50]}...")
            return enhanced_prompt
            
        except Exception as e:
            logger.warning(f"Failed to enhance prompt with Dify: {e}")
            # Return the original prompt if enhancement fails
            return prompt