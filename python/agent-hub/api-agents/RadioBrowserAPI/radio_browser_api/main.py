from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, List, Optional

@run_agent
def run(agent: MofaAgent):
    """
    Agent for interacting with the Radio-Browser API to fetch server lists, track station clicks,
    and search stations by country code.
    """
    try:
        # Input handling
        action = agent.receive_parameter('action')
        
        if action == 'get_servers':
            # Fetch list of available radio-browser servers
            url = "https://api.radio-browser.info/json/servers"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                servers = response.json()
                agent.send_output(
                    agent_output_name='server_list',
                    agent_result={"servers": servers}
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result={"error": f"Request to {url} failed with status code: {response.status_code}"}
                )
        
        elif action == 'track_click':
            # Track station popularity by recording a click
            station_uuid = agent.receive_parameter('station_uuid')
            url = f"https://de1.api.radio-browser.info/json/url/{station_uuid}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                agent.send_output(
                    agent_output_name='click_result',
                    agent_result={"status": "success", "data": response.json()}
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result={"error": f"Request to {url} failed with status code: {response.status_code}"}
                )
        
        elif action == 'search_stations':
            # Search radio stations by country code
            country_code = agent.receive_parameter('country_code')
            url = f"https://fr1.api.radio-browser.info/json/stations/search?countrycode={country_code}"
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                stations = response.json()
                agent.send_output(
                    agent_output_name='station_list',
                    agent_result={"stations": stations, "country_code": country_code}
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result={"error": f"Request to {url} failed with status code: {response.status_code}"}
                )
        
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={"error": "Invalid action specified. Valid actions: get_servers, track_click, search_stations"}
            )
    
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": f"An unexpected error occurred: {str(e)}"}
        )

def main():
    agent = MofaAgent(agent_name='RadioBrowserAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()