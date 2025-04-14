from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        input_param = agent.receive_parameter('query')
        
        # Determine the type of query (list, id, or seed)
        if input_param.startswith('list:'):
            limit = input_param.split(':')[1]
            url = f"https://picsum.photos/v2/list?limit={limit}"
            response = requests.get(url)
            if response.status_code == 200:
                images = response.json()
                agent.send_output(
                    agent_output_name='image_list',
                    agent_result=images
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        elif input_param.startswith('id:'):
            image_id = input_param.split(':')[1]
            url = f"https://picsum.photos/id/{image_id}/info"
            response = requests.get(url)
            if response.status_code == 200:
                details = response.json()
                agent.send_output(
                    agent_output_name='image_details',
                    agent_result=details
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        elif input_param.startswith('seed:'):
            seed = input_param.split(':')[1]
            url = f"https://picsum.photos/seed/{seed}/info"
            response = requests.get(url)
            if response.status_code == 200:
                details = response.json()
                agent.send_output(
                    agent_output_name='seeded_image_details',
                    agent_result=details
                )
            else:
                agent.send_output(
                    agent_output_name='error',
                    agent_result=f"Request to {url} failed with status code: {response.status_code}"
                )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Invalid query format. Expected 'list:', 'id:', or 'seed:'"
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='ImageMetadataFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()