from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    Agent to query the ConceptNet API for semantic relationships of a given concept.
    Inputs:
    - 'concept': The concept to analyze (e.g., 'test').
    Outputs:
    - 'relationships': A list of semantic relationships for the given concept.
    """
    try:
        # Input handling
        concept = agent.receive_parameter('concept')
        if not concept:
            raise ValueError("No concept provided for analysis.")

        # API configuration
        base_url = "http://api.conceptnet.io"
        endpoint = "/query"
        params = {
            'start': f'/c/en/{concept}',
            'rel': '/r/RelatedTo'
        }

        # Query ConceptNet API
        response = requests.get(f"{base_url}{endpoint}", params=params)
        if response.status_code != 200:
            raise Exception(f"Request to ConceptNet API failed with status code: {response.status_code}")

        # Process response
        data = response.json()
        relationships = []
        for edge in data['edges'][:5]:  # Limit to first 5 relationships
            relationships.append({
                'start': edge['start']['label'],
                'relationship': edge['rel']['label'],
                'end': edge['end']['label']
            })

        # Output delivery
        agent.send_output(
            agent_output_name='relationships',
            agent_result=relationships
        )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='ConceptNetAnalyzer')
    run(agent=agent)

if __name__ == '__main__':
    main()