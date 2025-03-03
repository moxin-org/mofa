from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch activity from Bored API
        response = requests.get('https://www.boredapi.com/api/activity')
        response.raise_for_status()
        activity_data = response.json()

        # Send the activity suggestion as output
        agent.send_output(
            agent_output_name='activity_suggestion',
            agent_result=activity_data
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='Bored-API')
    run(agent=agent)

if __name__ == '__main__':
    main()