from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from datetime import datetime
from typing import Dict, Any, Optional

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        base_currency = agent.receive_parameter('base_currency')
        date_range = agent.receive_parameter('date_range')
        target_currency = agent.receive_parameter('target_currency')

        # Validate inputs
        if not all([base_currency, date_range, target_currency]):
            raise ValueError("Missing required parameters: base_currency, date_range, target_currency")

        # Determine API endpoint based on date_range
        if ".." in date_range:
            # Time series endpoint
            url = f"https://api.frankfurter.dev/v1/{date_range}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rates_data = {
                    "base": data.get("base", "EUR"),
                    "rates": {
                        date: rates.get(target_currency) for date, rates in data.get("rates", {}).items()
                    }
                }
                agent.send_output(
                    agent_output_name='exchange_rates',
                    agent_result=rates_data
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        else:
            # Historical or latest endpoint
            if date_range.lower() == "latest":
                url = f"https://api.frankfurter.dev/v1/latest?from={base_currency}"
            else:
                url = f"https://api.frankfurter.dev/v1/{date_range}?from={base_currency}"

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rates_data = {
                    "base": data.get("base", "EUR"),
                    "date": data.get("date", date_range),
                    "rate": data.get("rates", {}).get(target_currency)
                }
                agent.send_output(
                    agent_output_name='exchange_rates',
                    agent_result=rates_data
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='CurrencyExchangeAnalyzer')
    run(agent=agent)

if __name__ == '__main__':
    main()