from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os
from typing import Dict, Any

def capture_screenshot(api_url: str, params: Dict[str, Any]) -> str:
    """
    Capture a screenshot using the Screenshotlayer API.
    
    Args:
        api_url (str): The base URL of the API endpoint.
        params (Dict[str, Any]): Parameters for the API request.
    
    Returns:
        str: The URL of the captured screenshot.
    
    Raises:
        Exception: If the API request fails.
    """
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json().get("screenshot_url", "")
    else:
        raise Exception(f"API request failed with status code: {response.status_code}")

@run_agent
def run(agent: MofaAgent):
    """
    Main execution function for the ScreenshotCaptureAgent.
    
    Args:
        agent (MofaAgent): The agent instance.
    """
    try:
        # Load environment variables
        access_key = os.getenv("ACCESS_KEY")
        if not access_key:
            raise ValueError("ACCESS_KEY environment variable not set.")
        
        # Receive input parameters
        params = agent.receive_parameters(["url", "viewport", "fullpage", "format"])
        
        # Prepare API parameters
        api_params = {
            "access_key": access_key,
            "url": params.get("url", "https://example.com"),
            "viewport": params.get("viewport", "1440x900"),
            "fullpage": int(params.get("fullpage", 1)),
            "format": params.get("format", "PNG")
        }
        
        # Capture screenshot
        api_url = "http://api.screenshotlayer.com/api/capture"
        screenshot_url = capture_screenshot(api_url, api_params)
        
        # Send output
        agent.send_output(
            agent_output_name="screenshot_url",
            agent_result=screenshot_url
        )
    except Exception as e:
        agent.send_output(
            agent_output_name="error",
            agent_result=str(e)
        )

def main():
    """
    Initialize and run the ScreenshotCaptureAgent.
    """
    agent = MofaAgent(agent_name="ScreenshotCaptureAgent")
    run(agent=agent)

if __name__ == "__main__":
    main()