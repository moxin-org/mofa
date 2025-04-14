from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Fetch the random duck image
        url = "https://random-d.uk/api/randomimg"
        response = requests.get(url)

        if response.status_code == 200:
            # Send the image bytes as output
            agent.send_output(
                agent_output_name='duck_image',
                agent_result={
                    'image_bytes': response.content,
                    'status': 'success'
                }
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={
                    'error': f"Request to {url} failed with status code: {response.status_code}",
                    'status': 'failed'
                }
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={
                'error': str(e),
                'status': 'failed'
            }
        )

def main():
    agent = MofaAgent(agent_name='DuckImageFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()