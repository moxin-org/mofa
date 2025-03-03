from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch joke from JokeAPI
        response = requests.get('https://v2.jokeapi.dev/joke/Any')
        response.raise_for_status()
        joke_data = response.json()

        # Send joke data to output port
        agent.send_output(
            agent_output_name='joke_data',
            agent_result=joke_data
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='JokeAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()