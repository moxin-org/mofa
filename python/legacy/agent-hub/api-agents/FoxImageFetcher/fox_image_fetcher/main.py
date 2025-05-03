from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch random fox image URL from API
        url = "https://randomfox.ca/floof"
        response = requests.get(url)

        if response.status_code == 200:
            fox_data = response.json()
            fox_image_url = fox_data["image"]
            agent.send_output(
                agent_output_name='fox_image_url',
                agent_result=fox_image_url
            )
        else:
            error_msg = f"Request to {url} failed with status code: {response.status_code}"
            agent.send_output(
                agent_output_name='error',
                agent_result=error_msg
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='FoxImageFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()