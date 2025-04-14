from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import logging
from typing import Optional, Dict, Any

@run_agent
def run(agent: MofaAgent):
    """
    TextProcessor Agent for interacting with the Exude API for text processing.
    Supports text filtering, file filtering, and swear word detection.
    """
    try:
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger = logging.getLogger("TextProcessor")

        # Receive input parameters
        operation = agent.receive_parameter('operation')
        input_data = agent.receive_parameter('input_data')

        # Validate operation type
        if operation not in ['text_filter', 'file_filter', 'swear_detection']:
            raise ValueError(f"Invalid operation: {operation}. Must be one of ['text_filter', 'file_filter', 'swear_detection']")

        # Process based on operation type
        if operation == 'text_filter':
            result = process_text_filter(input_data)
        elif operation == 'file_filter':
            result = process_file_filter(input_data)
        elif operation == 'swear_detection':
            result = process_swear_detection(input_data)

        # Send output
        agent.send_output(
            agent_output_name='processed_data',
            agent_result=result
        )

    except Exception as e:
        logger.error(f"Error in TextProcessor Agent: {str(e)}")
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def process_text_filter(text: str) -> Dict[str, Any]:
    """Process text filtering using the Exude API."""
    url = "https://exude.herokuapp.com/api/exude"
    payload = {"data": text}
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def process_file_filter(file_path: str) -> Dict[str, Any]:
    """Process file filtering using the Exude API."""
    url = "https://exude.herokuapp.com/api/exude-file"
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()

def process_swear_detection(text: str) -> Dict[str, Any]:
    """Process swear word detection using the Exude API."""
    url = "https://exude.herokuapp.com/api/exude-swear"
    payload = {"data": text}
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

def main():
    agent = MofaAgent(agent_name='TextProcessor')
    run(agent=agent)

if __name__ == '__main__':
    main()