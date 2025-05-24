"""
Integrated workflow module that coordinates all components.
"""
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# Import our separate components
from .image_generator import ImageGenerator
from .video_generator import VideoGenerator
from .music_generator import MusicGenerator
from .dify_enhancer import DifyEnhancer
from .keyframe_processor import KeyframeData

logger = logging.getLogger(__name__)

class IntegratedWorkflow:
    """Integrated workflow that coordinates all processing components."""
    
    def __init__(self, kling_config: Dict[str, Any], output_dir: Path, use_dify: bool = False, 
                 beatoven_api_key: Optional[str] = None, beatoven_api_url: Optional[str] = None,
                 music_prompt: Optional[str] = None, music_filename: Optional[str] = "background_music",
                 beatoven_env_file: Optional[str] = None):
        """
        Initialize the integrated workflow with all required components.
        
        Args:
            kling_config: Configuration for KlingDemo clients
            output_dir: Directory to save the generated files
            use_dify: Whether to use Dify for enhancing descriptions
            beatoven_api_key: API key for Beatoven (overrides env_file settings)
            beatoven_api_url: API URL for Beatoven (overrides env_file settings)
            music_prompt: Single music prompt for the entire workflow
            music_filename: Filename for the generated music
            beatoven_env_file: Path to environment file for Beatoven settings
        """
        self.output_dir = output_dir
        self.images_dir = output_dir / "images"
        self.videos_dir = output_dir / "videos"
        self.music_dir = output_dir / "music"
        self.use_dify = use_dify
        self.music_prompt = music_prompt
        self.music_filename = music_filename
        
        # Create necessary directories
        self.images_dir.mkdir(exist_ok=True, parents=True)
        self.videos_dir.mkdir(exist_ok=True, parents=True)
        self.music_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize all components
        self.image_generator = ImageGenerator(kling_config, self.images_dir)
        self.video_generator = VideoGenerator(kling_config, self.videos_dir)
        self.music_generator = MusicGenerator(
            api_key=beatoven_api_key, 
            api_url=beatoven_api_url, 
            output_dir=self.music_dir,
            env_file=beatoven_env_file
        )
        
        # Initialize Dify enhancer if enabled
        self.dify_enhancer = DifyEnhancer() if use_dify else None
        
        logger.info(f"Integrated workflow initialized. Dify integration: {'enabled' if use_dify else 'disabled'}")

    async def process_keyframes(self, keyframes_data: List[KeyframeData], 
                               model_name: str = "kling-v1-5") -> Dict[str, Dict[str, str]]:
        """
        Process keyframes to generate images, videos, and music.
        
        Args:
            keyframes_data: List of keyframe data
            model_name: Model name for image generation
            
        Returns:
            Dictionary mapping frame IDs to paths of generated assets
        """
        results = {}
        music_path = None
        
        # Generate a single music track for the entire workflow if a prompt is provided
        if self.music_prompt:
            try:
                logger.info(f"Generating music with prompt: {self.music_prompt[:50]}...")
                music_path = await self.music_generator.generate(
                    prompt=self.music_prompt,
                    duration=180,
                    format="mp3",
                    filename=self.music_filename
                )
                logger.info(f"Music generated at: {music_path}")
            except Exception as e:
                logger.error(f"Failed to generate music: {e}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Process each keyframe for images and videos
        for idx, keyframe in enumerate(keyframes_data):
            # Generate a frame_id based on frame_number or timestamp if not available
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if hasattr(keyframe, 'frame_number') and keyframe.frame_number is not None:
                frame_id = f"frame_{keyframe.frame_number}"
            else:
                frame_id = f"frame_{idx+1}_{timestamp}"
                
            logger.info(f"Processing keyframe {frame_id}: {keyframe.prompt[:30]}...")
            
            # Extract parameters from keyframe
            aspect_ratio = keyframe.aspect_ratio or "16:9"
            seed = keyframe.seed
            negative_prompt = keyframe.negative_prompt or ""
            
            # Generate image
            image_path = await self.image_generator.generate(
                prompt=keyframe.prompt,
                model_name=model_name,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                seed=seed,
                frame_id=frame_id
            )
            
            # Generate video from image if image was successfully generated
            video_path = None
            if image_path:
                # Enhance prompt with Dify if enabled
                prompt_for_video = keyframe.prompt
                if self.use_dify and self.dify_enhancer:
                    try:
                        prompt_for_video = self.dify_enhancer.enhance_prompt(keyframe.prompt)
                        logger.info(f"Enhanced prompt for video: {prompt_for_video[:50]}...")
                    except Exception as e:
                        logger.warning(f"Failed to enhance prompt with Dify: {e}. Using original prompt.")
                
                video_path = await self.video_generator.generate_from_image(
                    image_path=image_path,
                    prompt=prompt_for_video,
                    frame_id=frame_id
                )
                
            # Store results
            results[frame_id] = {
                'image': str(image_path) if image_path else None,
                'video': str(video_path) if video_path else None,
            }
            
        # Add the music path to all results
        if music_path:
            for frame_id in results:
                results[frame_id]['music'] = str(music_path)
        
        return results