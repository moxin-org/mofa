from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, List, Optional

@run_agent
def run(agent: MofaAgent):
    """
    Fetches university data from the universities.hipolabs.com API based on the provided name and country.
    """
    try:
        # Receive input parameters
        params = agent.receive_parameters(['university_name', 'country'])
        university_name = params.get('university_name', '')
        country = params.get('country', '')

        # Validate inputs
        if not university_name or not country:
            raise ValueError("Both 'university_name' and 'country' parameters are required.")

        # Construct API URL
        url = f"http://universities.hipolabs.com/search?name={university_name}&country={country}"

        # Fetch data from API
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code: {response.status_code}")

        # Process and send the response
        universities = response.json()
        if not universities:
            agent.send_output('university_data', {"message": "No universities found matching the criteria."})
        else:
            # Extract relevant data (e.g., name, domains, web_pages)
            processed_data = [
                {
                    "name": uni.get("name", ""),
                    "domains": uni.get("domains", []),
                    "web_pages": uni.get("web_pages", []),
                    "country": uni.get("country", "")
                }
                for uni in universities
            ]
            agent.send_output('university_data', processed_data)

    except Exception as e:
        agent.send_output('error', {"error": str(e)})

def main():
    agent = MofaAgent(agent_name='UniversityDataFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()