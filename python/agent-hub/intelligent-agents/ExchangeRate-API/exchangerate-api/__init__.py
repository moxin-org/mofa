from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Get API key from environment variables
        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError('API_KEY environment variable is not set')

        # Make API request
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'
        response = requests.get(url)
        response.raise_for_status()

        # Process response
        exchange_rates = response.json()

        # Send output
        agent.send_output(
            agent_output_name='exchange_rates',
            agent_result=exchange_rates
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'API request failed: {str(e)}'
        )
    except ValueError as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'Unexpected error: {str(e)}'
        )

def main():
    agent = MofaAgent(agent_name='ExchangeRate-API')
    run(agent=agent)

if __name__ == '__main__':
    main()