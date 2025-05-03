from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    Agent to fetch brewery data from the Open Brewery DB API.
    Handles API requests, processes the response, and sends the data as output.
    """
    try:
        # Input handling (if any parameters are needed)
        # Example: query_param = agent.receive_parameter('query')

        # API request
        url = "https://api.openbrewerydb.org/v1/breweries"
        response = requests.get(url)

        if response.status_code == 200:
            breweries = response.json()
            # Ensure the output is serializable
            processed_data = [
                {
                    "name": brewery.get("name", ""),
                    "city": brewery.get("city", ""),
                    "state": brewery.get("state", ""),
                    "country": brewery.get("country", ""),
                }
                for brewery in breweries
            ]

            # Output delivery
            agent.send_output(
                agent_output_name="brewery_data",
                agent_result=processed_data
            )
        else:
            agent.send_output(
                agent_output_name="error",
                agent_result={"error": f"API request failed with status code: {response.status_code}"}
            )
    except Exception as e:
        agent.send_output(
            agent_output_name="error",
            agent_result={"error": f"An unexpected error occurred: {str(e)}"}
        )

def main():
    agent = MofaAgent(agent_name="BreweryDataFetcher")
    run(agent=agent)

if __name__ == "__main__":
    main()