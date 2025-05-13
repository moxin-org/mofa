"""Main workflow for the Euterpe library.

This module contains the EuterpeWorkflow class that orchestrates the video generation process.
"""

import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union

# Import components from the refactored package structure
from euterpe.models import VideoGenerationRequest, VideoGenerationResult, EuterpeConfig, Keyframe
from euterpe.config_loader import load_config
from euterpe.enhancers.dify_client import DifyClient
from euterpe.generators.image_module import ImageGenerator, ImageGeneratorConfig
from euterpe.generators.music_module import MusicGenerator, MusicGeneratorConfig
from euterpe.generators.video_assembler import VideoAssembler, VideoAssemblerConfig
from euterpe.processors.keyframe_rules import KeyframeProcessor

# Set up logger
logger = logging.getLogger(__name__)


class EuterpeWorkflow:
    """Orchestrates the video generation process.
    
    This class coordinates the processing of keyframes, image generation, 
    video assembly, and optional music generation.
    """
    
    def __init__(self, config: Optional[EuterpeConfig] = None, request: Optional[VideoGenerationRequest] = None):
        """Initialize the workflow with configuration and request parameters.
        
        Args:
            config: Optional configuration with API keys and settings.
                If not provided, a default config will be loaded.
            request: Optional video generation request. Can be set later with set_request().
        """
        # Load configuration
        self.config = config if config is not None else load_config()
        self.request = request
        
        # Set up directories
        self.output_dir = Path(self.config.output_dir)
        self.images_dir = self.output_dir / "images"
        self.videos_dir = self.output_dir / "videos" 
        self.music_dir = self.output_dir / "music"
        
        # Create necessary directories
        self.images_dir.mkdir(exist_ok=True, parents=True)
        self.videos_dir.mkdir(exist_ok=True, parents=True)
        self.music_dir.mkdir(exist_ok=True, parents=True)
        
        # Initialize components
        self._init_components()
        
        logger.info(f"EuterpeWorkflow initialized. Dify enhancement: {'enabled' if self.config.use_dify_enhancement else 'disabled'}")
    
    def _init_components(self) -> None:
        """Initialize all workflow components based on the configuration."""
        # Initialize Kling client for image generation
        image_config = ImageGeneratorConfig(
            api_key=self.config.kling_api_key,
            base_url=self.config.kling_base_url,
            output_dir=self.images_dir
        )
        self.image_generator = ImageGenerator(image_config)
        
        # Initialize video assembler
        video_config = VideoAssemblerConfig(
            output_dir=self.videos_dir,
            temp_dir=self.output_dir / "temp"
        )
        self.video_assembler = VideoAssembler(video_config)
        
        # Initialize music generator
        music_config = MusicGeneratorConfig(
            api_key=self.config.beatoven_api_key,
            api_url=self.config.beatoven_api_url,
            output_dir=self.music_dir
        )
        self.music_generator = MusicGenerator(music_config)
        
        # Initialize Dify client for prompt enhancement if enabled
        self.dify_client = None
        if self.config.use_dify_enhancement and self.config.dify_api_key:
            self.dify_client = DifyClient()
        
        # Initialize keyframe processor
        self.keyframe_processor = KeyframeProcessor()
    
    def set_request(self, request: VideoGenerationRequest) -> None:
        """Set or update the video generation request.
        
        Args:
            request: The video generation request to process.
        """
        self.request = request
    
    async def run(self) -> Dict[str, Any]:
        """Run the workflow to generate video from keyframes and optional music.
        
        Returns:
            Dict[str, Any]: Dictionary with paths to generated files and metadata.
            
        Raises:
            ValueError: If no request has been set.
            Exception: For various processing errors.
        """
        if not self.request:
            raise ValueError("No video generation request has been set. Call set_request() first.")
        
        # Track results for each keyframe
        results = {}
        music_path = None
          # Generate music if prompt is provided
        if self.request.music_prompt:
            try:
                logger.info(f"Generating music with prompt: {self.request.music_prompt[:50]}...")
                # Get music duration from music_params if available, otherwise use default
                duration = None
                if hasattr(self.request, 'music_params') and self.request.music_params:
                    duration = getattr(self.request.music_params, 'duration', None)
                
                music_path = await self.music_generator.generate(
                    prompt=self.request.music_prompt,
                    duration=duration,  # This will default to the generator's config if None
                    filename=f"{self.request.output_filename}_music"
                )
                logger.info(f"Music generated at: {music_path}")
            except Exception as e:
                logger.error(f"Failed to generate music: {e}")
                logger.exception("Music generation failed")
        
        # Process each keyframe
        for idx, keyframe in enumerate(self.request.keyframes):
            frame_id = keyframe.frame_id
            logger.info(f"Processing keyframe {frame_id}: {keyframe.prompt[:30]}...")
            
            # Generate image
            try:
                image_path = await self.image_generator.generate(
                    prompt=keyframe.prompt,
                    negative_prompt=keyframe.negative_prompt,
                    aspect_ratio=keyframe.aspect_ratio,
                    seed=keyframe.seed,
                    frame_id=frame_id
                )
                
                # Generate video from image
                if image_path:
                    # Enhance prompt with Dify if enabled
                    prompt_for_video = keyframe.prompt
                    if self.request.enhance_prompts and self.dify_client:
                        try:
                            enhanced_prompt = self.dify_client.enhance_prompt(keyframe.prompt)
                            if enhanced_prompt:
                                prompt_for_video = enhanced_prompt
                                logger.info(f"Enhanced prompt for video: {prompt_for_video[:50]}...")
                        except Exception as e:
                            logger.warning(f"Failed to enhance prompt with Dify: {e}. Using original prompt.")
                    
                    video_path = await self.video_assembler.assemble_video(
                        [image_path],
                        output_filename=f"{self.request.output_filename}_{frame_id}",
                        music_path=music_path
                    )
                    
                    # Store results
                    results[frame_id] = {
                        'image_path': str(image_path),
                        'video_path': str(video_path) if video_path else None,
                        'timestamp': keyframe.timestamp,
                        'prompt': keyframe.prompt
                    }
                
            except Exception as e:
                logger.error(f"Failed to process keyframe {frame_id}: {e}")
                logger.exception("Keyframe processing failed")
        
        # Add music path to results if generated
        if music_path:
            results['music_path'] = str(music_path)
        
        # Extract paths for the result
        image_paths = [data['image_path'] for data in results.values() 
                      if isinstance(data, dict) and 'image_path' in data]
        video_paths = [data['video_path'] for data in results.values() 
                      if isinstance(data, dict) and 'video_path' in data and data['video_path']]
        
        return {
            'image_filepaths': image_paths,
            'video_filepaths': video_paths,
            'music_filepath': str(music_path) if music_path else None,
            'frame_details': results
        }
        
    def process(self, request: Optional[VideoGenerationRequest] = None) -> VideoGenerationResult:
        """Process a video generation request.
        
        This is the main synchronous entry point that runs the async workflow.
        
        Args:
            request: Optional video generation request. If not provided,
                    uses the request set in the constructor or with set_request().
                    
        Returns:
            VideoGenerationResult: Result with file paths and status.
            
        Raises:
            ValueError: If no request is provided or set.
        """
        if request:
            self.set_request(request)
            
        if not self.request:
            return VideoGenerationResult(
                success=False,
                message="No video generation request has been set.",
                error_details="Call set_request() first or provide a request to process()."
            )
            
        try:
            # Generate a timestamp for this run
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            run_id = f"{self.request.output_filename}_{timestamp}"
            
            logger.info(f"Starting video generation process with ID: {run_id}")
            
            # Run the async workflow
            result_data = asyncio.run(self.run())
            
            # Process the full video if multiple keyframes
            final_video_path = None
            if len(result_data['video_filepaths']) > 1:
                logger.info("Assembling complete video from keyframes...")
                try:
                    # Sort keyframe videos by timestamp
                    frame_details = {
                        k: v for k, v in result_data['frame_details'].items() 
                        if isinstance(v, dict) and 'timestamp' in v
                    }
                    sorted_videos = sorted(
                        [(k, v) for k, v in frame_details.items()], 
                        key=lambda x: x[1]['timestamp']
                    )
                    video_paths = [v['video_path'] for _, v in sorted_videos if v['video_path']]
                    
                    # Generate the final video
                    if video_paths:
                        video_params = self.request.get_video_parameters()
                        final_video_path = self.video_assembler.merge_videos(
                            video_paths, 
                            output_filename=self.request.output_filename,
                            music_path=result_data['music_filepath'] if video_params.include_audio else None,
                            fps=video_params.fps
                        )
                        logger.info(f"Final video assembled: {final_video_path}")
                except Exception as e:
                    logger.error(f"Failed to assemble final video: {e}")
                    logger.exception("Final video assembly failed")
            elif len(result_data['video_filepaths']) == 1:
                final_video_path = result_data['video_filepaths'][0]
            
            # Build and return the result
            metadata = {
                "total_keyframes": len(self.request.keyframes),
                "processed_keyframes": len([v for k, v in result_data['frame_details'].items() 
                                         if isinstance(v, dict) and 'image_path' in v]),
                "run_id": run_id,
                "timestamp": timestamp,
                "enhanced_prompts": self.request.enhance_prompts
            }
            
            result = VideoGenerationResult(
                success=True,
                message="Video generation completed successfully.",
                video_filepath=final_video_path or result_data['video_filepaths'][-1] if result_data['video_filepaths'] else None,
                music_filepath=result_data['music_filepath'],
                image_filepaths=result_data['image_filepaths'],
                metadata=metadata
            )
            return result
            
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            
            logger.error(f"Video generation failed: {str(e)}")
            logger.debug(f"Traceback: {error_traceback}")
            
            return VideoGenerationResult(
                success=False,
                message=f"Video generation failed: {type(e).__name__}",
                error_details=f"{str(e)}\n\nTraceback:\n{error_traceback}",
                metadata={"error_type": str(type(e).__name__)}
            )
