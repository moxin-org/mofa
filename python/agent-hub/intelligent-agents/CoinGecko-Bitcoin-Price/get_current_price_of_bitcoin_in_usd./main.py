from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch Bitcoin price from CoinGecko API
        response = requests.get(
            'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd'
        )
        response.raise_for_status()
        data = response.json()
        bitcoin_price = data.get('bitcoin', {}).get('usd')

        if bitcoin_price is None:
            raise ValueError('Bitcoin price not found in API response')

        # Send output
        agent.send_output(
            agent_output_name='bitcoin_price',
            agent_result=str(bitcoin_price)
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
    agent = MofaAgent(agent_name='CoinGecko-Bitcoin-Price')
    run(agent=agent)

if __name__ == '__main__':
    main()