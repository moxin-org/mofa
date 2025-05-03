from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any, Optional

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        operation = agent.receive_parameter('operation')
        params = agent.receive_parameters(['query', 'lat', 'lon', 'osm_ids'])

        # Validate operation
        if operation not in ['search', 'reverse', 'lookup']:
            raise ValueError(f"Invalid operation: {operation}. Must be 'search', 'reverse', or 'lookup'.")

        # Core logic
        api_url = f"https://nominatim.openstreetmap.org/{operation}"
        headers = {'User-Agent': 'NominatimGeocoder'}
        api_params = {'format': 'json'}

        # Add parameters based on operation
        if operation == 'search':
            api_params['q'] = params.get('query')
        elif operation == 'reverse':
            api_params['lat'] = params.get('lat')
            api_params['lon'] = params.get('lon')
        elif operation == 'lookup':
            api_params['osm_ids'] = params.get('osm_ids')

        # Make API request
        response = requests.get(api_url, params=api_params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                agent.send_output(
                    agent_output_name='api_response',
                    agent_result=data
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result={'error': 'No data found in the response.'}
                )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={'error': f"Request failed with status code: {response.status_code}"}
            )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )

def main():
    agent = MofaAgent(agent_name='NominatimGeocoder')
    run(agent=agent)

if __name__ == '__main__':
    main()