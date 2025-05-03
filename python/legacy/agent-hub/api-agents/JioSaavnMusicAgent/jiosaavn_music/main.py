from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class JioSaavnMusicAgent(MofaAgent):
    """
    A dora-rs compliant Agent for interacting with the JioSaavn API.
    Supports searching songs, fetching song details, and retrieving playlist contents.
    """

    def __init__(self, agent_name: str):
        super().__init__(agent_name=agent_name)
        self.api_base_url = "https://saavn.dev/api"
        self.endpoints = {
            "search_songs": "/search/songs",
            "song_details": "/songs/{song_id}",
            "playlist": "/playlists/{playlist_id}",
        }
        self.request_timeout = 30  # Timeout in seconds

    def _make_api_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an API request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to call.
            params (Optional[Dict[str, Any]]): Query parameters for the request.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        url = f"{self.api_base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=self.request_timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

@run_agent
def run(agent: JioSaavnMusicAgent):
    """
    Main execution function for the JioSaavnMusicAgent.
    """
    try:
        # Receive input parameters
        action = agent.receive_parameter("action")
        query = agent.receive_parameter("query")

        # Process based on action
        if action == "search_songs":
            endpoint = agent.endpoints["search_songs"]
            params = {"query": query}
            data = agent._make_api_request(endpoint, params)
            agent.send_output("search_results", data)

        elif action == "song_details":
            endpoint = agent.endpoints["song_details"].replace("{song_id}", query)
            data = agent._make_api_request(endpoint)
            agent.send_output("song_details", data)

        elif action == "playlist":
            endpoint = agent.endpoints["playlist"].replace("{playlist_id}", query)
            data = agent._make_api_request(endpoint)
            agent.send_output("playlist_contents", data)

        else:
            logger.error(f"Invalid action: {action}")
            agent.send_output("error", {"message": f"Invalid action: {action}"})

    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        agent.send_output("error", {"message": str(e)})

def main():
    agent = JioSaavnMusicAgent(agent_name="JioSaavnMusicAgent")
    run(agent=agent)

if __name__ == "__main__":
    main()