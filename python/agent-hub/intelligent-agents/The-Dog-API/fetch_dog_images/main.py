from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch random dog images
        response = requests.get('https://api.thedogapi.com/v1/images/search')
        response.raise_for_status()
        dog_images = response.json()

        # Send output
        agent.send_output(
            agent_output_name='dog_images',
            agent_result=json.dumps(dog_images)
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='The-Dog-API')
    run(agent=agent)

if __name__ == '__main__':
    main()