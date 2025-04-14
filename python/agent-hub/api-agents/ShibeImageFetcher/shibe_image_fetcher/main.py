from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling - optional parameter for count of images
        count = agent.receive_parameter('count')
        if count is None:
            count = 1  # Default to 1 image if no count is provided
        else:
            count = int(count)  # Ensure count is an integer

        # API call to fetch shibe images
        url = f"http://shibe.online/api/shibes?count={count}"
        response = requests.get(url)

        if response.status_code == 200:
            shibe_urls = response.json()
            agent.send_output(
                agent_output_name='shibe_images',
                agent_result=shibe_urls
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Request to {url} failed with status code: {response.status_code}"
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='ShibeImageFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()