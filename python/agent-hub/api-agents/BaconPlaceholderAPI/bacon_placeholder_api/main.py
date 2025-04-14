from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling - receive dimensions or use defaults
        dimensions = agent.receive_parameters(['width', 'height'])
        width = dimensions.get('width', 800)
        height = dimensions.get('height', 600)

        # Ensure dimensions are integers
        try:
            width = int(width)
            height = int(height)
        except ValueError as e:
            raise ValueError(f"Invalid dimensions provided: {e}")

        # Construct the URL
        url = f"https://baconmockup.com/{width}/{height}"

        # Fetch the image
        response = requests.get(url)

        if response.status_code == 200:
            # Send the image content as output
            agent.send_output(
                agent_output_name='image_content',
                agent_result={
                    'content': response.content,
                    'message': "Bacon placeholder image fetched successfully"
                }
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result={
                    'message': f"Request to {url} failed with status code: {response.status_code}"
                }
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={
                'message': f"An unexpected error occurred: {str(e)}"
            }
        )

def main():
    agent = MofaAgent(agent_name='BaconPlaceholderAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()