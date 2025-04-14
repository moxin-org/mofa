from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling - determine the type of joke request
        joke_type = agent.receive_parameter('joke_type')

        # API configuration
        api_endpoints = {
            "random_joke": "https://icanhazdadjoke.com/",
            "search_jokes": "https://icanhazdadjoke.com/search",
            "slack_joke": "https://icanhazdadjoke.com/slack"
        }

        default_headers = {
            "random_joke": {
                "Accept": "application/json",
                "User-Agent": "Python Script (https://example.com/contact)"
            },
            "search_jokes": {
                "Accept": "application/json",
                "User-Agent": "Python Script (https://example.com/contact)"
            },
            "slack_joke": {
                "User-Agent": "Python Slack Bot (https://example.com/contact)"
            }
        }

        search_params = {
            "term": "chicken",
            "limit": 3
        }

        # Process joke request based on type
        if joke_type == "random":
            response = requests.get(api_endpoints["random_joke"], headers=default_headers["random_joke"])
            if response.status_code == 200:
                data = response.json()
                agent.send_output(
                    agent_output_name='joke_response',
                    agent_result={"id": data["id"], "joke": data["joke"]}
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request failed with status code: {response.status_code}"
                )

        elif joke_type == "search":
            # Optional search term and limit from parameters
            search_term = agent.receive_parameter('search_term', default=search_params["term"])
            limit = agent.receive_parameter('limit', default=search_params["limit"])

            params = {
                "term": search_term,
                "limit": limit
            }

            response = requests.get(api_endpoints["search_jokes"], headers=default_headers["search_jokes"], params=params)
            if response.status_code == 200:
                results = response.json()["results"]
                agent.send_output(
                    agent_output_name='joke_response',
                    agent_result=[{"joke": joke["joke"]} for joke in results]
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Search failed with status code: {response.status_code}"
                )

        elif joke_type == "slack":
            response = requests.get(api_endpoints["slack_joke"], headers=default_headers["slack_joke"])
            if response.status_code == 200:
                slack_data = response.json()
                agent.send_output(
                    agent_output_name='joke_response',
                    agent_result={"text": slack_data["attachments"][0]["text"]}
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Slack request failed with status code: {response.status_code}"
                )

        else:
            agent.send_output(
                agent_output_name='error',
                agent_result="Invalid joke type specified. Use 'random', 'search', or 'slack'."
            )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An unexpected error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='DadJokeFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()