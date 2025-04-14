from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    Stack Exchange API Agent for interacting with Stack Overflow.
    Supports fetching questions, user profiles, and advanced search.
    """
    try:
        # Receive input parameters
        input_params = agent.receive_parameters(['action', 'query', 'user_id'])
        action = input_params.get('action')
        query = input_params.get('query')
        user_id = input_params.get('user_id')

        # Validate action
        if action not in ['questions', 'user', 'search']:
            raise ValueError("Invalid action. Must be 'questions', 'user', or 'search'.")

        # Initialize API parameters
        base_url = "https://api.stackexchange.com/2.3"
        params = {
            "site": "stackoverflow",
            "order": "desc",
            "sort": "activity",
            "pagesize": 5
        }

        # Handle actions
        if action == 'questions':
            # Fetch recent questions
            url = f"{base_url}/questions"
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                agent.send_output('questions_output', data)
            else:
                agent.send_output('error_output', f"Request failed with status code: {response.status_code}")

        elif action == 'user':
            # Fetch user profile
            if not user_id:
                raise ValueError("User ID is required for 'user' action.")
            url = f"{base_url}/users/{user_id}"
            params["filter"] = "!9_bDDxJY5"  # Custom filter for basic profile data
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                agent.send_output('user_output', data)
            else:
                agent.send_output('error_output', f"Request failed with status code: {response.status_code}")

        elif action == 'search':
            # Advanced search
            if not query:
                raise ValueError("Query is required for 'search' action.")
            url = f"{base_url}/search/advanced"
            params.update({
                "q": query,
                "accepted": "true",
                "pagesize": 3
            })
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                agent.send_output('search_output', data)
            else:
                agent.send_output('error_output', f"Request failed with status code: {response.status_code}")

    except Exception as e:
        agent.send_output('error_output', str(e))

def main():
    agent = MofaAgent(agent_name='StackExchangeAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()