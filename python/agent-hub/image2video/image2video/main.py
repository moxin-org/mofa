from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv, set_key  # 需要安装 python-dotenv

# Import from euterpe-creator package
from euterpe import (
    generate_video,
    VideoGenerationRequest,
    EuterpeConfig,
)

@run_agent
def run(agent: MofaAgent):
    """Main function for video generation using config from specified .env path.
    
    Args:
        agent: The MoFA agent instance
    """
    try:
        # Receive config path from start-input
        params = agent.receive_parameter('trigger_params')
        agent.logger.info(f"Received parameters: {params}")

        # Parse parameters
        if isinstance(params, str):
            params = json.loads(params)
        
        config_path = params.get('config_path')
        if not config_path:
            agent.logger.error("Missing config_path in trigger_params")
            agent.send_output(
                agent_output_name='video_result_out',
                agent_result=json.dumps({"error": "Missing config_path in trigger_params"})
            )
            return

        # Load config from specified .env file
        env_file = Path(config_path)
        if not env_file.is_file():
            agent.logger.error(f"Config file not found: {config_path}")
            agent.send_output(
                agent_output_name='video_result_out',
                agent_result=json.dumps({"error": f"Config file not found: {config_path}"})
            )
            return
        
        load_dotenv(env_file)
        
        # Extract required parameters
        image_path = os.getenv('IMAGE_PATH')
        prompt = os.getenv('PROMPT')
        output_dir = os.getenv('OUTPUT_DIR', './euterpe_output')
        
        if not image_path or not prompt:
            agent.logger.error("Missing IMAGE_PATH or PROMPT in .env file")
            agent.send_output(
                agent_output_name='video_result_out',
                agent_result=json.dumps({"error": "Missing IMAGE_PATH or PROMPT in .env file"})
            )
            return
        
        # Validate image_path
        image_path = Path(image_path)
        if not image_path.is_file():
            agent.logger.error("Invalid IMAGE_PATH: file does not exist")
            agent.send_output(
                agent_output_name='video_result_out',
                agent_result=json.dumps({"error": "Invalid IMAGE_PATH: file does not exist"})
            )
            return
        
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        # Create configuration
        config = EuterpeConfig(
            output_dir=output_dir,
            kling_api_key=os.getenv('KLING_API_KEY'),
        )
        
        # Create video generation request
        request = VideoGenerationRequest(
            keyframes=[{
                "image_path": str(image_path),
                "prompt": prompt
            }],
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
        }
        
        # Write output to output.env
        output_env_file = output_dir / "output.env"
        set_key(output_env_file, "SUCCESS", str(response["success"]))
        set_key(output_env_file, "MESSAGE", response["message"])
        set_key(output_env_file, "VIDEO_PATH", response["video_path"] or "")
        set_key(output_env_file, "IMAGE_PATHS", json.dumps(response["image_paths"]))
        
        agent.logger.info(f"Video generation completed with result: {result.success}")
        
        # Send the response
        agent.send_output(
            agent_output_name='video_result_out',
            agent_result=json.dumps(response)
        )
        
    except Exception as e:
        agent.logger.error(f"Error in video generation: {str(e)}")
        output_env_file = Path(output_dir) / "output.env" if 'output_dir' in locals() else Path("output.env")
        set_key(output_env_file, "SUCCESS", "False")
        set_key(output_env_file, "ERROR", str(e))
        agent.send_output(
            agent_output_name='video_result_out',
            agent_result=json.dumps({
                "success": False,
                "error": str(e)
            })
        )

def main():
    """Entry point for the video generation agent."""
    agent = MofaAgent(agent_name='video-generator')
    run(agent=agent)

if __name__ == "__main__":
    main()