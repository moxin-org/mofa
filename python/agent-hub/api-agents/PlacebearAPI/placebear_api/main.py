from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive parameters from the dataflow
        params = agent.receive_parameters(['width', 'height', 'filename'])
        width = int(params.get('width', 800))  # Default to 800 if not provided
        height = int(params.get('height', 600))  # Default to 600 if not provided
        filename = params.get('filename', 'bear_placeholder.jpg')  # Default filename

        # Construct the URL for the Placebear API
        url = f"https://placebear.com/g/{width}/{height}"

        # Fetch the image from the API
        response = requests.get(url)

        if response.status_code == 200:
            # Send the image data as output
            agent.send_output(
                agent_output_name='image_data',
                agent_result={
                    'image_data': response.content,
                    'filename': filename
                }
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
    agent = MofaAgent(agent_name='PlacebearAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()