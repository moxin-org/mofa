"""Video assembly module for the Euterpe library.

This module handles assembling images into videos and adding music tracks using FFmpeg.
"""

import asyncio
import logging
import os
import shutil
import uuid
from pathlib import Path
from typing import List, Optional, Union, Dict, Any

from pydantic import BaseModel, Field

# Set up logger
logger = logging.getLogger(__name__)


class VideoAssemblerConfig(BaseModel):
    """Configuration for the video assembler."""
    output_dir: Path = Field(default=Path("./output/videos"))
    temp_dir: Path = Field(default=Path("./output/temp"))
    ffmpeg_path: Optional[str] = None
    default_fps: float = 24.0
    default_resolution: Optional[str] = None  # e.g. "1920x1080"
    default_format: str = "mp4"
    default_video_codec: str = "libx264"
    default_audio_codec: str = "aac"

    class Config:
        validate_assignment = True


class VideoAssembler:
    """Assemble images into videos and add music tracks using FFmpeg."""
    
    def __init__(self, config: VideoAssemblerConfig):
        """Initialize the video assembler.
        
        Args:
            config: Configuration for the video assembler.
        """
        self.config = config
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        self.config.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Import ffmpeg-python here to ensure it's available
        try:
            import ffmpeg
            self.ffmpeg = ffmpeg
            logger.info("FFmpeg-python is available for video assembly")
        except ImportError:
            logger.error("ffmpeg-python is required but not installed")
            raise ImportError("ffmpeg-python is required for VideoAssembler")
            
        # Check if ffmpeg is actually available in the system
        try:
            version = self.ffmpeg.probe("version", v="error")
            logger.debug("FFmpeg is available in the system")
        except Exception:
            logger.warning("FFmpeg may not be properly installed in the system")
        
    async def assemble_video(
        self,
        image_paths: List[Path],
        output_filename: str = "output_video",
        fps: float = None,
        duration: Optional[float] = None,
        music_path: Optional[Path] = None,
        resolution: Optional[str] = None,
        format: Optional[str] = None,
        video_codec: Optional[str] = None,
        audio_codec: Optional[str] = None,
    ) -> Optional[Path]:
        """Assemble images into a video and optionally add a music track.
        
        Args:
            image_paths: List of paths to image files.
            output_filename: Output file name without extension.
            fps: Frames per second. If None, uses default_fps.
            duration: Optional total duration in seconds.
            music_path: Optional path to a music file to add.
            resolution: Optional output resolution (e.g., "1920x1080").
            format: Output format (e.g., "mp4", "mov").
            video_codec: Video codec to use.
            audio_codec: Audio codec to use.
            
        Returns:
            Path: Path to the generated video file, or None if assembly fails.
            
        Raises:
            Exception: If video assembly fails.
        """
        if not image_paths:
            logger.error("No image paths provided for video assembly")
            return None
            
        try:
            # Use defaults if parameters not provided
            fps = fps or self.config.default_fps
            format = format or self.config.default_format
            video_codec = video_codec or self.config.default_video_codec
            audio_codec = audio_codec or self.config.default_audio_codec
            resolution = resolution or self.config.default_resolution
            
            # Prepare output path
            output_file = self.config.output_dir / f"{output_filename}.{format}"
            
            # For a single image, create a slideshow
            if len(image_paths) == 1:
                logger.info(f"Creating video from single image: {image_paths[0]}")
                return await self._create_slideshow_from_image(
                    image_path=image_paths[0],
                    output_file=output_file,
                    duration=duration or 5.0,  # Default to 5 seconds if not specified
                    fps=fps,
                    music_path=music_path,
                    resolution=resolution,
                    video_codec=video_codec,
                    audio_codec=audio_codec
                )
            
            # For multiple images, create a slideshow
            logger.info(f"Creating video from {len(image_paths)} images")
            return await self._create_slideshow_from_images(
                image_paths=image_paths,
                output_file=output_file,
                duration=duration,
                fps=fps,
                music_path=music_path,
                resolution=resolution,
                video_codec=video_codec,
                audio_codec=audio_codec
            )
            
        except Exception as e:
            logger.error(f"Error assembling video: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    async def _create_slideshow_from_image(
        self,
        image_path: Path,
        output_file: Path,
        duration: float,
        fps: float,
        music_path: Optional[Path] = None,
        resolution: Optional[str] = None,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
    ) -> Optional[Path]:
        """Create a video slideshow from a single image.
        
        Args:
            image_path: Path to the image file.
            output_file: Path to the output video file.
            duration: Duration of the slideshow in seconds.
            fps: Frames per second.
            music_path: Optional path to a music file to add.
            resolution: Optional output resolution (e.g., "1920x1080").
            video_codec: Video codec to use.
            audio_codec: Audio codec to use.
            
        Returns:
            Path: Path to the generated video file, or None if assembly fails.
        """
        try:
            # Prepare FFmpeg input
            input_stream = self.ffmpeg.input(str(image_path), loop=1, t=duration)
            
            # Apply resolution if provided
            video_stream = input_stream.filter('fps', fps=fps)
            if resolution:
                width, height = map(int, resolution.split('x'))
                video_stream = video_stream.filter('scale', width, height)
            
            # Prepare output parameters
            output_args = {
                'c:v': video_codec,
                'pix_fmt': 'yuv420p',  # Required for compatibility
                'shortest': None,
                'y': None  # Overwrite output file
            }
            
            if music_path and music_path.exists():
                # Add audio stream if music is provided
                logger.info(f"Adding music track: {music_path}")
                audio_stream = self.ffmpeg.input(str(music_path))
                self.ffmpeg.output(
                    video_stream, 
                    audio_stream, 
                    str(output_file),
                    **output_args, 
                    c='copy', 
                    c_a=audio_codec
                ).run(quiet=True)
            else:
                # Output without audio
                self.ffmpeg.output(
                    video_stream, 
                    str(output_file),
                    **output_args
                ).run(quiet=True)
            
            logger.info(f"Video slideshow created at: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error creating slideshow from image: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    async def _create_slideshow_from_images(
        self,
        image_paths: List[Path],
        output_file: Path,
        duration: Optional[float] = None,
        fps: float = 24.0,
        music_path: Optional[Path] = None,
        resolution: Optional[str] = None,
        video_codec: str = "libx264",
        audio_codec: str = "aac",
    ) -> Optional[Path]:
        """Create a video slideshow from multiple images.
        
        Args:
            image_paths: List of paths to image files.
            output_file: Path to the output video file.
            duration: Optional total duration in seconds.
            fps: Frames per second.
            music_path: Optional path to a music file to add.
            resolution: Optional output resolution (e.g., "1920x1080").
            video_codec: Video codec to use.
            audio_codec: Audio codec to use.
            
        Returns:
            Path: Path to the generated video file, or None if assembly fails.
        """
        try:
            # Create a temporary directory for processing
            temp_dir = self.config.temp_dir / f"slideshow_{uuid.uuid4().hex}"
            temp_dir.mkdir(exist_ok=True, parents=True)
            
            try:
                # Calculate duration per image if total duration is specified
                images_count = len(image_paths)
                if duration:
                    # Leave some time for transitions
                    image_duration = max(1.0, duration / images_count)
                else:
                    # Default to 5 seconds per image
                    image_duration = 5.0
                    duration = image_duration * images_count
                
                # Create a concat file for FFmpeg
                concat_file = temp_dir / "concat.txt"
                with open(concat_file, "w") as f:
                    for img_path in image_paths:
                        # Each image needs to appear for image_duration seconds
                        f.write(f"file '{img_path}'\n")
                        f.write(f"duration {image_duration}\n")
                    # Add the last image again to ensure it's displayed
                    if image_paths:
                        f.write(f"file '{image_paths[-1]}'\n")
                
                # Prepare FFmpeg command
                cmd = self.ffmpeg.input(str(concat_file), format='concat', safe=0)
                
                # Apply filters
                video_stream = cmd.filter('fps', fps=fps)
                if resolution:
                    width, height = map(int, resolution.split('x'))
                    video_stream = video_stream.filter('scale', width, height)
                
                # Prepare output parameters
                output_args = {
                    'c:v': video_codec,
                    'pix_fmt': 'yuv420p',  # Required for compatibility
                    'y': None  # Overwrite output file
                }
                
                if music_path and music_path.exists():
                    # Add audio stream if music is provided
                    logger.info(f"Adding music track: {music_path}")
                    audio_stream = self.ffmpeg.input(str(music_path))
                    
                    # Ensure audio doesn't exceed video duration
                    audio_stream = audio_stream.filter('atrim', duration=duration)
                    
                    self.ffmpeg.output(
                        video_stream, 
                        audio_stream, 
                        str(output_file),
                        **output_args,
                        c_a=audio_codec,
                        shortest=None
                    ).run(quiet=True)
                else:
                    # Output without audio
                    self.ffmpeg.output(
                        video_stream, 
                        str(output_file),
                        **output_args
                    ).run(quiet=True)
                
                logger.info(f"Video slideshow created at: {output_file}")
                return output_file
                
            finally:
                # Clean up temporary directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    
        except Exception as e:
            logger.error(f"Error creating slideshow from images: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
            
    def merge_videos(
        self,
        video_paths: List[str],
        output_filename: str = "merged_video",
        music_path: Optional[Path] = None,
        format: str = "mp4",
        fps: Optional[float] = None,
        video_codec: Optional[str] = None,
    ) -> Optional[Path]:
        """Merge multiple videos into a single video.
        
        Args:
            video_paths: List of paths to video files.
            output_filename: Output file name without extension.
            music_path: Optional path to a music file to add.
            format: Output format (e.g., "mp4", "mov").
            fps: Optional frames per second for the output.
            video_codec: Optional video codec to use.
            
        Returns:
            Path: Path to the merged video file, or None if merging fails.
        """
        if not video_paths:
            logger.error("No video paths provided for merging")
            return None
            
        try:
            # Use defaults if parameters not provided
            fps = fps or self.config.default_fps
            video_codec = video_codec or self.config.default_video_codec
            format = format or self.config.default_format
            
            # Prepare output path
            output_file = self.config.output_dir / f"{output_filename}.{format}"
            
            # Create a temporary directory for processing
            temp_dir = self.config.temp_dir / f"merge_{uuid.uuid4().hex}"
            temp_dir.mkdir(exist_ok=True, parents=True)
            
            try:
                # Create a concat file for FFmpeg
                concat_file = temp_dir / "concat.txt"
                with open(concat_file, "w") as f:
                    for video_path in video_paths:
                        f.write(f"file '{video_path}'\n")
                
                # Basic merging without re-encoding if possible
                if music_path and music_path.exists():
                    # If we need to add music, we need to re-encode
                    # First, concatenate the videos
                    temp_video = temp_dir / f"temp_video.{format}"
                    self.ffmpeg.input(
                        str(concat_file), 
                        format='concat', 
                        safe=0
                    ).output(
                        str(temp_video),
                        c='copy'
                    ).run(quiet=True)
                      # Then add the music track
                    audio_stream = self.ffmpeg.input(str(music_path))
                    video_stream = self.ffmpeg.input(str(temp_video))
                    self.ffmpeg.output(
                        video_stream,
                        audio_stream,
                        str(output_file),
                        c='copy',
                        map=['0:v:0', '1:a:0'],
                        shortest=None,
                        y=None
                    ).run(quiet=True)
                else:
                    # Simple concatenation without re-encoding
                    self.ffmpeg.input(
                        str(concat_file), 
                        format='concat', 
                        safe=0
                    ).output(
                        str(output_file),
                        c='copy',
                        y=None
                    ).run(quiet=True)
                
                logger.info(f"Videos merged successfully: {output_file}")
                return output_file
                
            finally:
                # Clean up temporary directory
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    
        except Exception as e:
            logger.error(f"Error merging videos: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
