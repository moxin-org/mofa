from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any, Optional

@run_agent
def run(agent: MofaAgent):
    """
    Open Library API Handler Agent for dora-rs framework.
    This agent interacts with the Open Library API to fetch book details, author information, and search results.
    """
    try:
        # Receive input parameters from the dataflow
        input_params = agent.receive_parameters(['api_type', 'identifier', 'query'])
        api_type = input_params.get('api_type')
        identifier = input_params.get('identifier')
        query = input_params.get('query')

        # Validate input parameters
        if not api_type:
            raise ValueError("Missing required parameter: 'api_type'")

        # Initialize the base URL and endpoints from the configuration
        base_url = "https://openlibrary.org"
        endpoints = {
            "works": "/works/{work_id}.json",
            "authors": "/authors/{author_id}.json",
            "search": "/search.json"
        }

        # Construct the API URL based on the type of request
        if api_type == "works" and identifier:
            endpoint = endpoints["works"].format(work_id=identifier)
            url = f"{base_url}{endpoint}"
            response = requests.get(url)
        elif api_type == "authors" and identifier:
            endpoint = endpoints["authors"].format(author_id=identifier)
            url = f"{base_url}{endpoint}"
            response = requests.get(url)
        elif api_type == "search" and query:
            endpoint = endpoints["search"]
            url = f"{base_url}{endpoint}"
            params = {'q': query, 'limit': 10}
            response = requests.get(url, params=params)
        else:
            raise ValueError("Invalid or missing parameters for the API request")

        # Process the API response
        if response.status_code == 200:
            data = response.json()
            agent.send_output(
                agent_output_name='api_response',
                agent_result=data
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={
                    'error': f"API request failed with status code: {response.status_code}",
                    'url': url
                }
            )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={
                'error': str(e)
            }
        )

def main():
    agent = MofaAgent(agent_name='OpenLibraryAPIHandler')
    run(agent=agent)

if __name__ == '__main__':
    main()