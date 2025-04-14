from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os
from typing import Optional, Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    FOAASClient Agent for interacting with the FOAAS API.
    Handles requests to various endpoints including version info, operations, and protected resources.
    """
    try:
        # Load configuration from environment and YAML
        base_url = agent.receive_parameter('base_url')
        timeout = int(agent.receive_parameter('timeout'))
        default_headers = agent.receive_parameters(['Accept'])
        access_token = os.getenv('ACCESS_TOKEN')

        # Determine the endpoint to call based on input
        endpoint = agent.receive_parameter('endpoint')
        url = f"{base_url}/{endpoint}"

        # Prepare headers
        headers = default_headers
        if endpoint == "protected-resource":
            if not access_token:
                raise ValueError("ACCESS_TOKEN environment variable not set")
            headers["Authorization"] = f"Bearer {access_token}"

        # Make the API request
        response = requests.get(url, headers=headers, timeout=timeout)

        # Process the response
        if response.status_code == 200:
            processed_data = response.json()
            agent.send_output(
                agent_output_name='api_response',
                agent_result=processed_data
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={"status_code": response.status_code, "message": "API request failed"}
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": str(e)}
        )

def main():
    agent = MofaAgent(agent_name='FOAASClient')
    run(agent=agent)

if __name__ == '__main__':
    main()