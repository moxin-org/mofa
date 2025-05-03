from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling - receive the category parameter
        category = agent.receive_parameter('category')
        
        # Validate the category input
        if not category:
            raise ValueError("Category parameter is required")
        
        # Construct the API URL
        url = f"https://emojihub.yurace.pro/api/random/category/{category}"
        
        # Make the API request
        response = requests.get(url)
        
        # Check for successful response
        if response.status_code == 200:
            emoji_data = response.json()
            
            # Prepare the output data
            output_data = {
                "name": emoji_data["name"],
                "html_code": emoji_data["htmlCode"][0],
                "category": emoji_data["category"]
            }
            
            # Send the output
            agent.send_output(
                agent_output_name='emoji_data',
                agent_result=output_data
            )
        else:
            # Handle API errors
            error_message = f"Request to {url} failed with status code: {response.status_code}"
            agent.send_output(
                agent_output_name='error',
                agent_result=error_message
            )
    except Exception as e:
        # Handle unexpected errors
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='EmojiHubAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()