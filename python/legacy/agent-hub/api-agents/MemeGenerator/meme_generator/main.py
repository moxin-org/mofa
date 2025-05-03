from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os
from typing import Dict, List, Optional

@run_agent
def run(agent: MofaAgent):
    try:
        # Retrieve environment variables
        username = os.getenv("IMGFLIP_USERNAME")
        password = os.getenv("IMGFLIP_PASSWORD")
        premium_username = os.getenv("PREMIUM_IMGFLIP_USERNAME")
        premium_password = os.getenv("PREMIUM_IMGFLIP_PASSWORD")

        # Retrieve parameters from the dataflow
        action = agent.receive_parameter('action')

        if action == 'get_memes':
            # Fetch popular meme templates
            url = "https://api.imgflip.com/get_memes"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                memes = data.get('data', {}).get('memes', [])
                agent.send_output(
                    agent_output_name='meme_templates',
                    agent_result=memes
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )

        elif action == 'caption_image':
            # Generate a custom meme
            template_id = agent.receive_parameter('template_id')
            text0 = agent.receive_parameter('text0')
            text1 = agent.receive_parameter('text1')

            url = "https://api.imgflip.com/caption_image"
            payload = {
                'template_id': template_id,
                'username': username,
                'password': password,
                'text0': text0,
                'text1': text1
            }

            response = requests.post(url, data=payload)

            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    agent.send_output(
                        agent_output_name='meme_url',
                        agent_result=data['data']['url']
                    )
                else:
                    agent.send_output(
                        agent_output_name='error',
                        agent_result=f"Failed to create meme: {data.get('error_message', 'Unknown error')}"
                    )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )

        elif action == 'search_memes':
            # Search for memes (Premium feature)
            query = agent.receive_parameter('query')

            url = "https://api.imgflip.com/search_memes"
            payload = {
                'username': premium_username,
                'password': premium_password,
                'query': query
            }

            response = requests.post(url, data=payload)

            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    agent.send_output(
                        agent_output_name='search_results',
                        agent_result=data['data']['memes']
                    )
                else:
                    agent.send_output(
                        agent_output_name='error',
                        agent_result=f"Failed to search memes: {data.get('error_message', 'Unknown error')}"
                    )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )

        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Invalid action: {action}"
            )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An unexpected error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='MemeGenerator')
    run(agent=agent)

if __name__ == '__main__':
    main()