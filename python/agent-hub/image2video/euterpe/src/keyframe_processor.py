"""
Keyframe processing module for parsing and processing keyframe data.
"""
import sys
import os
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

# Add the keyframe parser from examples
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib', 'KlingDemo', 'src'))
try:
    from examples.keyframe_to_image.keyframe_parser import KeyframeData, parse_keyframe_file
except ImportError:
    logger.warning("Could not import keyframe parser from KlingDemo examples. Using a simplified version.")
    
    class KeyframeData:
        """Simple keyframe data class if the original is not available."""
        def __init__(self, prompt, negative_prompt=None, frame_number=None, 
                     timestamp=None, aspect_ratio=None, seed=None):
            self.prompt = prompt
            self.negative_prompt = negative_prompt
            self.frame_number = frame_number
            self.timestamp = timestamp
            self.aspect_ratio = aspect_ratio
            self.seed = seed
    
    def parse_keyframe_file(file_path):
        """Simple keyframe file parser if the original is not available."""
        keyframes = []
        current_frame = {}
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if line.startswith("---"):
                # New keyframe
                if current_frame and "prompt" in current_frame:
                    keyframes.append(KeyframeData(
                        prompt=current_frame.get("prompt", ""),
                        negative_prompt=current_frame.get("negative_prompt"),
                        frame_number=current_frame.get("frame_number"),
                        aspect_ratio=current_frame.get("aspect_ratio", "16:9"),
                        seed=current_frame.get("seed")
                    ))
                current_frame = {}
                continue
            
            # Parse key-value pairs
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower()
                value = value.strip()
                
                if key == "frame" or key == "frame_number":
                    try:
                        current_frame["frame_number"] = int(value)
                    except ValueError:
                        pass
                elif key == "prompt":
                    current_frame["prompt"] = value
                elif key == "negative_prompt":
                    current_frame["negative_prompt"] = value
                elif key == "aspect_ratio":
                    current_frame["aspect_ratio"] = value
                elif key == "seed":
                    try:
                        current_frame["seed"] = int(value)
                    except ValueError:
                        pass
        
        # Add the last keyframe
        if current_frame and "prompt" in current_frame:
            keyframes.append(KeyframeData(
                prompt=current_frame.get("prompt", ""),
                negative_prompt=current_frame.get("negative_prompt"),
                frame_number=current_frame.get("frame_number"),
                aspect_ratio=current_frame.get("aspect_ratio", "16:9"),
                seed=current_frame.get("seed")
            ))
            
        return keyframes

class KeyframeProcessor:
    """Handles keyframe parsing and processing."""
    
    def __init__(self):
        """Initialize the keyframe processor."""
        logger.info("Initialized keyframe processor")
    
    def parse_keyframes(self, keyframes_file: Path) -> List[KeyframeData]:
        """
        Parse a keyframes file.
        
        Args:
            keyframes_file: Path to the keyframes file
            
        Returns:
            List of parsed keyframe data
            
        Raises:
            ValueError: If the keyframes file does not exist
        """
        if not keyframes_file.is_file():
            raise ValueError(f"Keyframes file not found: {keyframes_file}")
            
        try:
            keyframes_data = parse_keyframe_file(keyframes_file)
            logger.info(f"Parsed {len(keyframes_data)} keyframes from {keyframes_file}")
            return keyframes_data
        except Exception as e:
            logger.error(f"Failed to parse keyframes file: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise