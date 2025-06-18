from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive cryptocurrency id as input string (e.g., 'bitcoin')
        crypto_id = agent.receive_parameter('crypto_id')
        # Sanitize input
        crypto_id = str(crypto_id).strip().lower()
        if not crypto_id:
            raise ValueError('crypto_id parameter is required.')

        # Prepare CoinGecko API request
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"

        # Send GET request
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check for valid response
        if crypto_id not in data or 'usd' not in data[crypto_id]:
            raise ValueError(f"Price data for '{crypto_id}' not found.")
        price = data[crypto_id]['usd']

        output = {
            'crypto_id': crypto_id,
            'usd_price': price
        }
        agent.send_output(
            agent_output_name='crypto_price',
            agent_result=output
        )
    except Exception as e:
        error_message = {'error': str(e)}
        agent.send_output(
            agent_output_name='crypto_price',
            agent_result=error_message
        )

def main():
    agent = MofaAgent(agent_name='RealTimeCryptoPriceAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()
