"""Main module for the Euterpe Agent.

This module implements a MoFA agent that interfaces with the euterpe-creator package
for generating videos from keyframes with optional music.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from mofa.agent_build.base.base_agent import MofaAgent, run_agent

# Import from euterpe-creator package
from euterpe import (
    generate_video,
    VideoGenerationRequest,
    EuterpeConfig,
    Keyframe,
    AspectRatio,
    MusicParams,
    ImageModel,
    DifyEnhancementParams,
)

@run_agent
def run(agent: MofaAgent):
    """Main function for the Euterpe agent.
    
    Args:
        agent: The MoFA agent instance
    """
    try:
        # Get parameters from the agent
        params = agent.receive_parameter('params')
        agent.logger.info(f"Received parameters: {params}")
        
        # Parse parameters
        if isinstance(params, str):
            try:
                params = json.loads(params)
            except json.JSONDecodeError:
                agent.logger.error(f"Failed to parse JSON parameters: {params}")
                agent.send_output(
                    agent_output_name='euterpe_result',
                    agent_result={"error": "Invalid JSON parameters"}
                )
                return
        
        # Extract parameters needed for Euterpe
        # Keyframes are required
        if 'keyframes' not in params:
            agent.logger.error("No keyframes provided in parameters")
            agent.send_output(
                agent_output_name='euterpe_result',
                agent_result={"error": "No keyframes provided"}
            )
            return
        
        # Create output directory
        output_dir = Path(params.get("output_dir", "./euterpe_output"))
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create keyframes
        keyframes = []
        for kf in params['keyframes']:
            keyframe = Keyframe(
                frame_id=kf.get('frame_id'),
                timestamp=kf.get('timestamp', 0.0),
                prompt=kf.get('prompt', ''),
                negative_prompt=kf.get('negative_prompt'),
                image_path=kf.get('image_path'),
            )
            keyframes.append(keyframe)
        
        # Create music parameters if provided
        music_params = None
        if 'music' in params:
            music_data = params['music']
            music_params = MusicParams(
                prompt=music_data.get('prompt', ''),
                duration=music_data.get('duration', 180.0),
                genre=music_data.get('genre'),
                tempo=music_data.get('tempo'),
                format=music_data.get('format', 'mp3'),
            )
        
        # Determine aspect ratio
        aspect_ratio = AspectRatio.LANDSCAPE
        if 'aspect_ratio' in params:
            aspect_ratio_str = params['aspect_ratio']
            if aspect_ratio_str in [ar.value for ar in AspectRatio]:
                aspect_ratio = AspectRatio(aspect_ratio_str)
        
        # Determine image model
        image_model = ImageModel.KLING_V1_5
        if 'image_model' in params:
            model_str = params['image_model']
            if model_str in [m.value for m in ImageModel]:
                image_model = ImageModel(model_str)
        
        # Check for Dify enhancement
        use_dify = params.get('use_dify', False)
        dify_params = None
        if use_dify and 'dify' in params:
            dify_data = params['dify']
            dify_params = DifyEnhancementParams(
                api_key=dify_data.get('api_key', os.environ.get('DIFY_API_KEY', '')),
                api_base_url=dify_data.get('api_base_url', os.environ.get('DIFY_API_BASE', '')),
                application_id=dify_data.get('application_id', os.environ.get('DIFY_APP_ID', '')),
            )
        
        # Create configuration
        config = EuterpeConfig(
            output_dir=output_dir,
            kling_api_key=os.environ.get('KLING_API_KEY'),
            beatoven_api_key=os.environ.get('BEATOVEN_API_KEY'),
        )
        
        # Create video generation request
        request = VideoGenerationRequest(
            keyframes=keyframes,
            music_params=music_params,
            aspect_ratio=aspect_ratio,
            image_model=image_model,
            dify_enhancement_params=dify_params,
            fps=params.get('fps', 30),
            resolution=params.get('resolution', 720),
        )
        
        # Generate the video
        agent.logger.info("Starting video generation...")
        result = generate_video(request, config)
        
        # Create response
        response = {
            "success": result.success,
            "message": result.message,
            "video_path": str(result.video_path) if result.video_path else None,
            "image_paths": [str(p) for p in result.image_paths],
            "music_path": str(result.music_path) if result.music_path else None,
        }
        
        agent.logger.info(f"Video generation completed with result: {result.success}")
        
        # Send the response
        agent.send_output(
            agent_output_name='euterpe_result',
            agent_result=json.dumps(response)
        )
        
    except Exception as e:
        agent.logger.error(f"Error in Euterpe agent: {str(e)}")
        agent.send_output(
            agent_output_name='euterpe_result',
            agent_result=json.dumps({
                "success": False,
                "error": str(e)
            })
        )

def main():
    """Entry point for the Euterpe agent."""
    agent = MofaAgent(agent_name='euterpe-agent')
    run(agent=agent)

if __name__ == "__main__":
    main()
