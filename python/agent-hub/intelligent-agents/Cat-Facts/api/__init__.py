from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch cat fact from API
        response = requests.get('https://catfact.ninja/fact')
        response.raise_for_status()
        cat_fact = response.json()['fact']

        # Send output
        agent.send_output(
            agent_output_name='cat_fact',
            agent_result=cat_fact
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'API request failed: {str(e)}'
        )
    except KeyError:
        agent.send_output(
            agent_output_name='error',
            agent_result='Invalid response format from API'
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'Unexpected error: {str(e)}'
        )

def main():
    agent = MofaAgent(agent_name='Cat-Facts')
    run(agent=agent)

if __name__ == '__main__':
    main()