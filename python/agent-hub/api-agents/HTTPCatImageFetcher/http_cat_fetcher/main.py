from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        status_code = agent.receive_parameter('status_code')
        
        # Validate and convert status_code to integer
        try:
            status_code = int(status_code)
        except ValueError:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Invalid status code: {status_code}. Must be an integer."
            )
            return
        
        # Core logic: Fetch HTTP cat image
        url = f"https://http.cat/{status_code}.jpg"
        response = requests.get(url)
        
        if response.status_code == 200:
            # Send the image content as bytes (serialized as base64)
            import base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            agent.send_output(
                agent_output_name='image_data',
                agent_result={
                    'status_code': status_code,
                    'image_base64': image_base64
                }
            )
        else:
            agent.send_output(
                agent_output_name='error',
                agent_result=f"Failed to fetch image for status code {status_code}. HTTP response: {response.status_code}"
            )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An unexpected error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='HTTPCatImageFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()