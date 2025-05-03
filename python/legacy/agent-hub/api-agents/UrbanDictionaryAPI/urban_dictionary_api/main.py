from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, List, Any

@run_agent
def run(agent: MofaAgent):
    """
    Urban Dictionary API Agent that fetches definitions for a given word.
    Inputs:
      - 'word': The word to fetch definitions for.
    Outputs:
      - 'definitions': A list of definitions (limited to max_definitions).
    """
    try:
        # Input handling
        word = agent.receive_parameter('word')
        if not word:
            raise ValueError("No word provided for definition lookup.")

        # Fetch configurations
        base_url = agent.receive_parameter('base_url')
        max_definitions = int(agent.receive_parameter('max_definitions'))

        # API request
        url = f"{base_url}/define?term={word}"
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code: {response.status_code}")

        # Process response
        data = response.json()
        definitions = []
        for definition in data.get('list', [])[:max_definitions]:
            definitions.append({
                'definition': definition.get('definition', ''),
                'example': definition.get('example', '')
            })

        # Output delivery
        agent.send_output(
            agent_output_name='definitions',
            agent_result=definitions
        )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='UrbanDictionaryAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()