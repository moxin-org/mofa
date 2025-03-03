from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        city = agent.receive_parameter('city')
        api_key = os.getenv('API_KEY')

        if not api_key:
            raise ValueError('API_KEY environment variable not set')

        # Core logic
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        # Output delivery
        agent.send_output(
            agent_output_name='weather_data',
            agent_result=weather_data
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
    agent = MofaAgent(agent_name='OpenWeatherMap-Current-Weather-Data')
    run(agent=agent)

if __name__ == '__main__':
    main()