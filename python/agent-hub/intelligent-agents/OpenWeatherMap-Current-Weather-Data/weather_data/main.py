from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        city_name = agent.receive_parameter('city_name')
        api_key = os.getenv('API_KEY')

        if not city_name or not api_key:
            raise ValueError('City name and API key are required')

        # API request
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
        response = requests.get(url)
        response.raise_for_status()

        # Output delivery
        agent.send_output(
            agent_output_name='weather_data',
            agent_result=response.json()
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
    agent = MofaAgent(agent_name='OpenWeatherMap-Current-Weather-Data')
    run(agent=agent)

if __name__ == '__main__':
    main()