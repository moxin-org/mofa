from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import os
from typing import Dict, List, Optional

@run_agent
def run(agent: MofaAgent):
    try:
        # Load environment variables
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable not set.")

        # Receive input parameters
        action = agent.receive_parameter("action")
        if action not in ["get_tags", "search_images", "get_favorites"]:
            raise ValueError("Invalid action specified. Valid actions: get_tags, search_images, get_favorites.")

        # Initialize API base URL from YAML config
        base_url = "https://api.waifu.im"

        if action == "get_tags":
            # Retrieve list of available tags
            url = f"{base_url}/tags"
            response = requests.get(url)
            if response.status_code == 200:
                tags = response.json().get("tags", [])
                agent.send_output(
                    agent_output_name="tags_list",
                    agent_result=[tag["name"] for tag in tags]
                )
            else:
                raise Exception(f"Request to {url} failed with status code: {response.status_code}")

        elif action == "search_images":
            # Search images by tags
            included_tags = agent.receive_parameter("included_tags")
            limit = agent.receive_parameter("limit")
            params = {
                "included_tags": included_tags,
                "limit": int(limit) if limit else 5
            }
            url = f"{base_url}/search"
            response = requests.get(url, params=params)
            if response.status_code == 200:
                images = response.json().get("images", [])
                agent.send_output(
                    agent_output_name="image_urls",
                    agent_result=[img["url"] for img in images]
                )
            else:
                raise Exception(f"Request to {url} failed with status code: {response.status_code}")

        elif action == "get_favorites":
            # Retrieve user's favorite images
            url = f"{base_url}/favorites"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                favorites = response.json().get("images", [])
                agent.send_output(
                    agent_output_name="favorites_list",
                    agent_result=[f["image_id"] for f in favorites]
                )
            else:
                raise Exception(f"Request to {url} failed with status code: {response.status_code}")

    except Exception as e:
        agent.send_output(
            agent_output_name="error",
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name="WaifuImageManager")
    run(agent=agent)

if __name__ == "__main__":
    main()