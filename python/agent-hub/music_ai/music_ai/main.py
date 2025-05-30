import os
import json
import logging
import requests
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from time import sleep

from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from euterpe import AspectRatio, MusicParams

@run_agent
def run(agent: MofaAgent):
    """Main function for the music-ai agent.
    
    Args:
        agent: The MoFA agent instance
    """
    try:
        params = agent.receive_parameter('params')
        #agent.logger.info(f"Received parameters: {params}")
        
        response = {
            "success": True,
            "music_params": None,
            "aspect_ratio": None,
            "music_output_path": None,
            "message": "Music parameters processed successfully"
        }
        
        env_file_path = params.strip() if isinstance(params, str) else ""
        music_data = {}
        
        if env_file_path:
            env_path = Path(env_file_path)
            if env_path.exists() and env_path.is_file():
                load_dotenv(env_path)
                music_prompt = os.getenv("MUSIC-PROMOT")
                music_output = os.getenv("MUSIC_OUTPUT")
                
                if music_prompt:
                    music_data["prompt"] = music_prompt
                    # agent.logger.info(f"Loaded MUSIC-PROMOT from .env: {music_prompt}")
                else:
                    # agent.logger.error("MUSIC-PROMOT not found in .env file")
                    response["success"] = False
                    response["message"] = "Missing MUSIC-PROMOT in .env file"
                    agent.send_output(
                        agent_output_name='music_ai_result',
                        agent_result=json.dumps(response)
                    )
                    return
                
                if music_output:
                    response["music_output_path"] = music_output
                    # agent.logger.info(f"Loaded MUSIC_OUTPUT from .env: {music_output}")
                else:
                    # agent.logger.warning("MUSIC_OUTPUT not found in .env file, using default output path")
                    pass
            else:
                # agent.logger.error(f"Invalid .env file path: {env_file_path}")
                response["success"] = False
                response["message"] = f"Invalid or missing .env file: {env_file_path}"
                agent.send_output(
                    agent_output_name='music_ai_result',
                    agent_result=json.dumps(response)
                )
                return
        else:
            # agent.logger.error("No .env file path provided")
            response["success"] = False
            response["message"] = "No .env file path provided"
            agent.send_output(
                agent_output_name='music_ai_result',
                agent_result=json.dumps(response)
            )
            return
        
        if response["music_output_path"]:
            output_dir = Path(response["music_output_path"]).parent
            output_music_path = Path(response["music_output_path"])
        else:
            output_dir = Path("./music_ai_output")
            output_music_path = output_dir / "generated_music.mp3"
        output_dir.mkdir(exist_ok=True, parents=True)
        
        music_params = MusicParams(
            prompt=music_data.get("prompt", ""),
            duration=float(os.getenv("BEATOVEN_DEFAULT_DURATION", 180.0)),
            genre=os.getenv("MUSIC_GENRE"),
            tempo=os.getenv("MUSIC_TEMPO"),
            format=os.getenv("BEATOVEN_DEFAULT_FORMAT", "mp3")
        )
        response["music_params"] = {
            "prompt": music_params.prompt,
            "duration": music_params.duration,
            "genre": music_params.genre,
            "tempo": music_params.tempo,
            "format": music_params.format
        }
        
        aspect_ratio = AspectRatio.LANDSCAPE
        aspect_ratio_str = os.getenv("ASPECT_RATIO")
        if aspect_ratio_str and aspect_ratio_str in [ar.value for ar in AspectRatio]:
            aspect_ratio = AspectRatio(aspect_ratio_str)
        else:
            # agent.logger.warning(f"Invalid or missing ASPECT_RATIO in .env: {aspect_ratio_str}, using default: LANDSCAPE")
            pass
        response["aspect_ratio"] = aspect_ratio.value
        
        try:
            api_key = os.getenv("BEATOVEN_API_KEY")
            api_url = os.getenv("BEATOVEN_API_URL")
            request_timeout = int(os.getenv("BEATOVEN_REQUEST_TIMEOUT", 30))
            download_timeout = int(os.getenv("BEATOVEN_DOWNLOAD_TIMEOUT", 60))
            polling_interval = int(os.getenv("BEATOVEN_POLLING_INTERVAL", 5))
            
            if not api_key or not api_url:
                raise ValueError("Missing BEATOVEN_API_KEY or BEATOVEN_API_URL in .env file")
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            payload = {
                "prompt": {"text": music_params.prompt},
                "duration": int(music_params.duration),
                "format": music_params.format
            }
            # agent.logger.info(f"Sending music generation request to Beatoven.ai: {payload}")
            job_response = requests.post(
                f"{api_url}/tracks/compose",
                headers=headers,
                json=payload,
                timeout=request_timeout
            )
            try:
                job_response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # agent.logger.error(f"API error response: {job_response.text}")
                raise
            
            job_data = job_response.json()
            task_id = job_data.get("task_id")
            if not task_id:
                raise ValueError("No task_id returned from Beatoven.ai API")
            
            status_url = f"{api_url}/tasks/{task_id}"
            for _ in range(download_timeout // polling_interval):
                status_response = requests.get(status_url, headers=headers, timeout=request_timeout)
                status_response.raise_for_status()
                status_data = status_response.json()
                status = status_data.get("status")
                if status == "composed":
                    music_url = status_data.get("meta", {}).get("track_url")
                    if not music_url:
                        raise ValueError("No track_url in composed job")
                    break
                elif status == "failed":
                    raise RuntimeError(f"Music generation failed: {status_data.get('error')}")
                sleep(polling_interval)
            else:
                raise TimeoutError("Music generation timed out")
            
            music_response = requests.get(music_url, timeout=download_timeout)
            music_response.raise_for_status()
            output_music_path.write_bytes(music_response.content)
            response["music_output_path"] = str(output_music_path)
            # agent.logger.info(f"Generated music saved to: {response['music_output_path']}")
            
        except Exception as e:
            # agent.logger.error(f"Failed to generate music with Beatoven.ai: {str(e)}")
            response["success"] = False
            response["message"] = f"Music generation failed: {str(e)}"
            agent.send_output(
                agent_output_name='music_ai_result',
                agent_result=json.dumps(response)
            )
            return
        
        # agent.logger.info(f"Music parameters processed: {response}")
        agent.send_output(
            agent_output_name='music_ai_result',
            agent_result=json.dumps(response)
        )
        
    except Exception as e:
        # agent.logger.error(f"Error in music-ai agent: {str(e)}")
        agent.send_output(
            agent_output_name='music_ai_result',
            agent_result=json.dumps({
                "success": False,
                "error": str(e)
            })
        )

def main():
    """Entry point for the music-ai agent."""
    agent = MofaAgent(agent_name='music-ai')
    run(agent=agent)

if __name__ == "__main__":
    main()
