from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from datetime import date

@run_agent
def run(agent: MofaAgent):
    try:
        # Determine the operation type from input parameters
        operation = agent.receive_parameter('operation')

        if operation == 'search':
            # Handle show search operation
            query = agent.receive_parameter('query')
            url = "https://api.tvmaze.com/search/shows"
            params = {'q': query}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                shows = response.json()
                processed_results = [
                    {
                        'name': show['show']['name'],
                        'premiered': show['show']['premiered'][:4] if show['show']['premiered'] else 'N/A'
                    }
                    for show in shows
                ]
                agent.send_output('search_results', processed_results)
            else:
                agent.send_output('error', f"Search failed with status code: {response.status_code}")

        elif operation == 'schedule':
            # Handle schedule retrieval operation
            country = agent.receive_parameter('country')
            schedule_date = agent.receive_parameter('date')
            url = "https://api.tvmaze.com/schedule"
            params = {'country': country, 'date': schedule_date}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                schedule = response.json()
                processed_results = [
                    {
                        'name': episode['name'],
                        'airtime': episode['airtime']
                    }
                    for episode in schedule
                ]
                agent.send_output('schedule_results', processed_results)
            else:
                agent.send_output('error', f"Schedule request failed with status code: {response.status_code}")

        elif operation == 'details':
            # Handle show details operation
            show_id = agent.receive_parameter('show_id')
            url = f"https://api.tvmaze.com/shows/{show_id}"
            response = requests.get(url)

            if response.status_code == 200:
                show_data = response.json()
                processed_results = {
                    'name': show_data['name'],
                    'genre': show_data['genres'][0] if show_data['genres'] else 'N/A',
                    'rating': show_data['rating']['average'] if show_data['rating'] else 'N/A',
                    'summary': show_data['summary']
                }
                agent.send_output('show_details', processed_results)
            else:
                agent.send_output('error', f"Show request failed with status code: {response.status_code}")

        else:
            agent.send_output('error', f"Invalid operation: {operation}")

    except Exception as e:
        agent.send_output('error', f"An error occurred: {str(e)}")

def main():
    agent = MofaAgent(agent_name='TVShowDataAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()