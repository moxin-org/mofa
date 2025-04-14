from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        query = agent.receive_parameter('query')
        api_key = os.getenv('XENO_CANTO_API_KEY')
        if not api_key:
            raise ValueError("Xeno-canto API key not found in environment variables")

        # API request
        endpoint = "https://xeno-canto.org/api/3/recordings"
        params = {
            "query": query if query else "sp:'troglodytes troglodytes' cnt:spain",
            "key": api_key,
            "per_page": 5
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()

        # Process response
        data = response.json()
        recordings = data.get('recordings', [])
        processed_data = []
        for recording in recordings:
            processed_data.append({
                "id": recording['id'],
                "species": recording['en'],
                "date": recording['date'],
                "location": recording['loc'],
                "audio_url": f"https:{recording['file']}"
            })

        # Output delivery
        agent.send_output(
            agent_output_name='recordings',
            agent_result=processed_data
        )

    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": f"API request failed: {str(e)}"}
        )
    except ValueError as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": str(e)}
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": f"Unexpected error: {str(e)}"}
        )

def main():
    agent = MofaAgent(agent_name='WildlifeSoundAnalyzer')
    run(agent=agent)

if __name__ == '__main__':
    main()