from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive the endpoint and optional query parameters
        endpoint = agent.receive_parameter('endpoint')
        query_params = agent.receive_parameter('query_params', optional=True)

        # Validate the endpoint
        if endpoint not in ['characters', 'locations', 'episodes']:
            raise ValueError(f"Invalid endpoint: {endpoint}. Must be one of ['characters', 'locations', 'episodes'].")

        # Construct the URL
        base_url = "https://rickandmortyapi.com/api"
        endpoint_map = {
            'characters': '/character',
            'locations': '/location',
            'episodes': '/episode'
        }
        url = f"{base_url}{endpoint_map[endpoint]}"

        # Add query parameters if provided
        if query_params:
            query_params = json.loads(query_params)  # Convert string to dict
            url += "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])

        # Make the API request
        response = requests.get(url, timeout=30)

        # Handle the response
        if response.status_code == 200:
            data = response.json()
            agent.send_output(
                agent_output_name='api_response',
                agent_result=json.dumps(data)  # Ensure serialization
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Request failed: {response.status_code}"
            )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='RickAndMortyAPIHandler')
    run(agent=agent)

if __name__ == '__main__':
    main()