from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch API key from environment variables
        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError('API_KEY environment variable not set')

        # Construct the API URL
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=' + api_key

        # Make the GET request
        response = requests.get(url)
        response.raise_for_status()

        # Parse the JSON response
        news_data = response.json()

        # Send the output
        agent.send_output(
            agent_output_name='news_data',
            agent_result=news_data
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )


def main():
    agent = MofaAgent(agent_name='News-API')
    run(agent=agent)

if __name__ == '__main__':
    main()