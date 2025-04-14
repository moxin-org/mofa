from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import logging
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    NameAnalysisAgent: Predicts age, gender, and nationality based on a given name using external APIs.
    """
    try:
        # Input handling
        name = agent.receive_parameter('name')
        if not name:
            raise ValueError("Name parameter is required.")

        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # API configurations
        api_endpoints = {
            'agify': "https://api.agify.io",
            'genderize': "https://api.genderize.io",
            'nationalize': "https://api.nationalize.io"
        }

        # Timeout setting
        timeout = 10

        # Initialize results dictionary
        results: Dict[str, Any] = {}

        # Function to call APIs
        def call_api(endpoint: str, params: Dict[str, str]) -> Dict[str, Any]:
            try:
                response = requests.get(api_endpoints[endpoint], params=params, timeout=timeout)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error(f"{endpoint} API request failed with status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                logger.error(f"{endpoint} API request failed: {str(e)}")
                return None

        # Call Agify API for age prediction
        age_data = call_api('agify', {'name': name})
        if age_data:
            results['age'] = age_data.get('age')
            results['name'] = age_data.get('name')

        # Call Genderize API for gender prediction
        gender_data = call_api('genderize', {'name': name})
        if gender_data:
            results['gender'] = gender_data.get('gender')
            results['gender_probability'] = gender_data.get('probability')

        # Call Nationalize API for nationality prediction
        nationality_data = call_api('nationalize', {'name': name})
        if nationality_data and nationality_data.get('country'):
            top_country = nationality_data['country'][0]
            results['nationality'] = top_country.get('country_id')
            results['nationality_probability'] = top_country.get('probability')

        # Output delivery
        agent.send_output(
            agent_output_name='analysis_results',
            agent_result=results
        )

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )

def main():
    agent = MofaAgent(agent_name='NameAnalysisAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()