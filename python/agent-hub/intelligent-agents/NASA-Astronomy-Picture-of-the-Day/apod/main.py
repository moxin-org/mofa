from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import requests
from datetime import datetime

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch API key from environment variables
        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError('API_KEY environment variable not set')

        # Make API request to NASA APOD
        response = requests.get(
            'https://api.nasa.gov/planetary/apod',
            params={'api_key': api_key}
        )
        response.raise_for_status()

        # Process and send output
        apod_data = response.json()
        agent.send_output(
            agent_output_name='apod_data',
            agent_result=apod_data
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )


def main():
    agent = MofaAgent(agent_name='NASA-Astronomy-Picture-of-the-Day')
    run(agent=agent)

if __name__ == '__main__':
    main()