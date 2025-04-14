from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Optional, List

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        params = agent.receive_parameters(['category', 'type', 'exclude', 'count'])
        category = params.get('category', 'waifu')
        request_type = params.get('type', 'sfw')
        exclude = params.get('exclude', [])
        count = params.get('count', 1)

        # Validate inputs
        if request_type not in ['sfw', 'nsfw']:
            raise ValueError("Type must be either 'sfw' or 'nsfw'.")
        if not isinstance(exclude, list):
            raise ValueError("Exclude must be a list of URLs.")
        if not isinstance(count, int) or count < 1:
            raise ValueError("Count must be a positive integer.")

        # Core logic
        if count == 1:
            # Single image request
            url = f"https://api.waifu.pics/{request_type}/{category}"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                agent.send_output('image_url', data['url'])
            else:
                agent.send_output('error', f"Request failed with status code: {response.status_code}")
        else:
            # Multiple images request
            url = "https://api.waifu.pics/many/{request_type}/{category}"
            payload = {"exclude": exclude} if exclude else {}
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                agent.send_output('image_urls', data['files'])
            else:
                agent.send_output('error', f"Request failed with status code: {response.status_code}")

    except Exception as e:
        agent.send_output('error', str(e))

def main():
    agent = MofaAgent(agent_name='WaifuImageFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()