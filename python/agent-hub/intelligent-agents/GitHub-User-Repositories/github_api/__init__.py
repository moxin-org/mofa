from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        username = agent.receive_parameter('username')

        # API call
        url = f'https://api.github.com/users/{username}/repos'
        response = requests.get(url)
        response.raise_for_status()

        # Process response
        repos = response.json()
        processed_data = [{'name': repo['name'], 'url': repo['html_url']} for repo in repos]

        # Output delivery
        agent.send_output(
            agent_output_name='repositories',
            agent_result=json.dumps(processed_data)
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )


def main():
    agent = MofaAgent(agent_name='GitHub-User-Repositories')
    run(agent=agent)

if __name__ == '__main__':
    main()