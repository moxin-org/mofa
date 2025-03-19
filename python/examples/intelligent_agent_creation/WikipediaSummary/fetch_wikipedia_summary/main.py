from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Dict, Any

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive topic parameter
        topic = agent.receive_parameter('topic')
        
        # Validate topic
        if not topic or not isinstance(topic, str):
            raise ValueError("Topic must be a non-empty string")
        
        # Fetch Wikipedia summary
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
        response = requests.get(url)
        response.raise_for_status()
        
        # Process response
        summary_data = response.json()
        processed_data = {
            'title': summary_data.get('title', ''),
            'summary': summary_data.get('extract', ''),
            'url': summary_data.get('content_urls', {}).get('desktop', {}).get('page', '')
        }
        
        # Send output
        agent.send_output(
            agent_output_name='wikipedia_summary',
            agent_result=processed_data
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': f"API request failed: {str(e)}"}
        )
    except ValueError as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )
    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': f"Unexpected error: {str(e)}"}
        )

def main():
    agent = MofaAgent(agent_name='WikipediaSummary')
    run(agent=agent)

if __name__ == '__main__':
    main()