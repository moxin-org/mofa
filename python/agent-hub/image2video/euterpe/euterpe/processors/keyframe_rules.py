"""Keyframe processing module for the Euterpe library.

This module handles parsing and processing of keyframe data for video generation.
"""

import logging
import re
import uuid
from typing import List, Optional, TextIO, Union, Dict, Any, Tuple
from pathlib import Path

from ..models import Keyframe, AspectRatio

# Set up logger
logger = logging.getLogger(__name__)


class KeyframeProcessor:
    """Process keyframe data for video generation."""
    
    def __init__(self):
        """Initialize the keyframe processor."""
        logger.info("Initialized keyframe processor")
    
    def parse_keyframes_file(self, file_path: Union[str, Path]) -> List[Keyframe]:
        """Parse a keyframes file into Keyframe objects.
        
        Args:
            file_path: Path to the keyframes file.
            
        Returns:
            List[Keyframe]: A list of parsed Keyframe objects.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file format is invalid.
        """
        # Convert string path to Path object if needed
        if isinstance(file_path, str):
            file_path = Path(file_path)
        
        # Check if the file exists
        if not file_path.exists():
            raise FileNotFoundError(f"Keyframes file not found: {file_path}")
        
        # Read the file and parse its content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse_keyframes_text(content)
            
        except Exception as e:
            logger.error(f"Failed to parse keyframes file {file_path}: {str(e)}")
            import traceback
            logger.debug(traceback.format_exc())
            raise ValueError(f"Failed to parse keyframes file: {str(e)}")
        
    def parse_keyframes_text(self, text: str) -> List[Keyframe]:
        """Parse keyframes from text content.
        
        Args:
            text: The keyframes text content.
            
        Returns:
            List[Keyframe]: A list of parsed Keyframe objects.
            
        Raises:
            ValueError: If the text format is invalid.
        """
        keyframes: List[Keyframe] = []
        
        # Split text into keyframe blocks
        blocks = self._split_into_blocks(text)
        
        # Parse each block
        for block_idx, block in enumerate(blocks):
            try:
                keyframe = self._parse_keyframe_block(block, block_idx)
                if keyframe:
                    keyframes.append(keyframe)
            except Exception as e:
                logger.warning(f"Failed to parse keyframe block {block_idx}: {str(e)}")
                logger.debug(f"Problematic block: {block}")
        
        # Sort keyframes by timestamp
        keyframes.sort(key=lambda k: k.timestamp)
        
        if not keyframes:
            raise ValueError("No valid keyframes found in the text")
        
        logger.info(f"Parsed {len(keyframes)} keyframes")
        return keyframes
    
    def _split_into_blocks(self, text: str) -> List[str]:
        """Split text content into keyframe blocks.
        
        Args:
            text: The keyframes text content.
            
        Returns:
            List[str]: A list of keyframe block texts.
        """
        # Remove comments
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            lines.append(line)
        
        # Join lines back and split by keyframe separator
        content = '\n'.join(lines)
        
        # Try different separator styles
        if '---' in content:
            blocks = re.split(r'---+', content)
        elif '===' in content:
            blocks = re.split(r'===+', content)
        else:
            # Assume each keyframe is separated by empty lines
            blocks = re.split(r'\n\s*\n+', content)
        
        # Remove empty blocks
        return [b.strip() for b in blocks if b.strip()]
    
    def _parse_keyframe_block(self, block: str, block_idx: int) -> Optional[Keyframe]:
        """Parse a keyframe block into a Keyframe object.
        
        Args:
            block: The keyframe block text.
            block_idx: The index of the block for generating IDs.
            
        Returns:
            Optional[Keyframe]: A Keyframe object, or None if parsing fails.
        """
        # Parse key-value pairs
        data: Dict[str, Any] = {}
        prompt_parts = []
        
        # Keep track of if we're inside a multi-line prompt
        in_prompt = False
        prompt_key = None
        
        for line in block.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in a multi-line prompt
            if in_prompt:
                # Check if the line ends the multi-line prompt
                if line.endswith('"""') or line.endswith("'''"):
                    prompt_parts.append(line[:-3].strip())
                    data[prompt_key] = '\n'.join(prompt_parts)
                    in_prompt = False
                    prompt_parts = []
                    prompt_key = None
                else:
                    prompt_parts.append(line)
                continue
            
            # Check if the line is a key-value pair
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                # Check for multi-line prompt start
                if value.startswith('"""') or value.startswith("'''"):
                    if value.endswith('"""') or value.endswith("'''") and len(value) > 6:
                        # Single line with quotes
                        data[key] = value[3:-3].strip()
                    else:
                        # Start of multi-line
                        in_prompt = True
                        prompt_key = key
                        if len(value) > 3:
                            prompt_parts.append(value[3:].strip())
                    continue
                
                # Process normal key-value pairs
                if key in ['prompt', 'negative_prompt']:
                    data[key] = value
                elif key in ['frame', 'frame_id', 'id']:
                    data['frame_id'] = value
                elif key in ['timestamp', 'time']:
                    try:
                        data['timestamp'] = float(value)
                    except ValueError:
                        logger.warning(f"Invalid timestamp value: {value}")
                elif key == 'aspect_ratio':
                    data['aspect_ratio'] = value
                elif key == 'seed':
                    try:
                        data['seed'] = int(value)
                    except ValueError:
                        logger.warning(f"Invalid seed value: {value}")
                elif key == 'weight':
                    try:
                        data['weight'] = float(value)
                    except ValueError:
                        logger.warning(f"Invalid weight value: {value}")
            else:
                # Line without a key - treat as part of the prompt
                if 'prompt' not in data:
                    data['prompt'] = line
                else:
                    data['prompt'] += f" {line}"
        
        # Check if we have the required fields
        if 'prompt' not in data:
            logger.warning(f"No prompt found in block {block_idx}")
            return None
        
        # Generate frame_id if not provided
        if 'frame_id' not in data:
            data['frame_id'] = f"frame_{block_idx}"
        
        # Generate timestamp if not provided
        if 'timestamp' not in data:
            data['timestamp'] = float(block_idx * 5)  # 5 seconds per keyframe
        
        # Create the keyframe object
        try:
            keyframe = Keyframe(
                frame_id=data['frame_id'],
                timestamp=data['timestamp'],
                prompt=data['prompt'],
                negative_prompt=data.get('negative_prompt'),
                aspect_ratio=data.get('aspect_ratio', AspectRatio.LANDSCAPE.value),
                seed=data.get('seed'),
                weight=data.get('weight', 1.0)
            )
            return keyframe
        except Exception as e:
            logger.warning(f"Failed to create Keyframe object: {str(e)}")
            return None
    
    def interpolate_keyframes(
        self, 
        keyframes: List[Keyframe], 
        fps: float = 24.0, 
        min_spacing: float = 1.0
    ) -> List[Keyframe]:
        """Interpolate between keyframes to generate smooth transitions.
        
        Args:
            keyframes: The list of input keyframes.
            fps: Frames per second for video generation.
            min_spacing: Minimum spacing between keyframes in seconds.
            
        Returns:
            List[Keyframe]: A list of keyframes including interpolated ones.
        """
        if len(keyframes) <= 1:
            return keyframes
            
        # Sort by timestamp
        sorted_keyframes = sorted(keyframes, key=lambda k: k.timestamp)
        
        result = [sorted_keyframes[0]]
        
        # Interpolate between consecutive keyframes
        for i in range(len(sorted_keyframes) - 1):
            start_kf = sorted_keyframes[i]
            end_kf = sorted_keyframes[i + 1]
            
            time_diff = end_kf.timestamp - start_kf.timestamp
            
            # Skip interpolation if keyframes are too close
            if time_diff < min_spacing:
                result.append(end_kf)
                continue
                
            # Calculate number of frames to insert
            num_frames = max(1, int(time_diff * fps / 4))  # 1 keyframe every 4 frames
            
            for j in range(1, num_frames):
                # Calculate interpolation factor
                t = j / num_frames
                
                # Interpolate timestamp
                timestamp = start_kf.timestamp + t * time_diff
                
                # Create interpolated keyframe with blend of prompts
                frame_id = f"interp_{i}_{j}"
                
                # Simply use the prompt from the nearest keyframe for now
                # In a more advanced implementation, we could blend the prompts
                closer_kf = start_kf if t < 0.5 else end_kf
                
                keyframe = Keyframe(
                    frame_id=frame_id,
                    timestamp=timestamp,
                    prompt=closer_kf.prompt,
                    negative_prompt=closer_kf.negative_prompt,
                    aspect_ratio=closer_kf.aspect_ratio,
                    seed=closer_kf.seed,
                    weight=0.5  # Lower weight for interpolated frames
                )
                result.append(keyframe)
            
            result.append(end_kf)
        
        # Sort again by timestamp to ensure order
        result.sort(key=lambda k: k.timestamp)
        
        logger.info(f"Generated {len(result)} keyframes with interpolation")
        return result
