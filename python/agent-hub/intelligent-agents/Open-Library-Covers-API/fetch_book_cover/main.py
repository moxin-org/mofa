from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        isbn = agent.receive_parameter('isbn')
        
        # Validate ISBN
        if not isbn or not isbn.strip():
            raise ValueError('ISBN parameter is required')
        
        # Construct API URL
        url = f'http://covers.openlibrary.org/b/ISBN/{isbn}-L.jpg'
        
        # Make API request
        response = requests.get(url)
        response.raise_for_status()
        
        # Send output
        agent.send_output(
            agent_output_name='book_cover',
            agent_result=response.content.decode('utf-8')
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'API request failed: {str(e)}'
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result=f'An error occurred: {str(e)}'
        )

def main():
    agent = MofaAgent(agent_name='Open-Library-Covers-API')
    run(agent=agent)

if __name__ == '__main__':
    main()