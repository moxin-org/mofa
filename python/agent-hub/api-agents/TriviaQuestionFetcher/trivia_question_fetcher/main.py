from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json
from typing import Dict, List, Optional

@run_agent
def run(agent: MofaAgent):
    """
    Fetches trivia questions from the Open Trivia Database API based on configured parameters.
    Handles input/output operations and error containment as per dora-rs framework standards.
    """
    try:
        # Fetch configuration parameters
        config = agent.receive_parameters(['base_url', 'question_params', 'endpoints', 'timeout'])
        base_url = config['base_url']
        question_params = config['question_params']
        endpoints = config['endpoints']
        timeout = config['timeout']

        # Construct the API URL for fetching questions
        questions_url = f"{base_url}{endpoints['questions']}?"
        questions_url += "&".join([f"{k}={v}" for k, v in question_params.items()])

        # Make the API request
        response = requests.get(questions_url, timeout=timeout)

        if response.status_code == 200:
            # Process the JSON response
            data = response.json()
            questions = data.get('results', [])
            
            # Send the processed questions as output
            agent.send_output(
                agent_output_name='trivia_questions',
                agent_result=json.dumps(questions)
            )
        else:
            # Handle API request failure
            error_msg = f"Request to {questions_url} failed with status code: {response.status_code}"
            agent.send_output(
                agent_output_name='error',
                agent_result=error_msg
            )
    except Exception as e:
        # Handle any unexpected errors
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='TriviaQuestionFetcher')
    run(agent=agent)

if __name__ == '__main__':
    main()