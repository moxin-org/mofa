from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
from typing import Optional, Dict, Union

@run_agent
def run(agent: MofaAgent):
    """
    Agent to interact with NumbersAPI, fetching trivia, math facts, or historical events.
    Inputs:
        - 'query_type': Type of query (trivia, math, date)
        - 'number': Number for trivia/math queries
        - 'month' and 'day': For date queries
    Outputs:
        - 'api_response': Response from NumbersAPI
    """
    try:
        # Receive input parameters
        params = agent.receive_parameters(['query_type', 'number', 'month', 'day'])
        query_type = params.get('query_type')
        number = params.get('number')
        month = params.get('month')
        day = params.get('day')

        # Validate inputs
        if not query_type:
            raise ValueError("Missing required parameter 'query_type'")

        # Construct API URL based on query type
        base_url = "http://numbersapi.com"
        if query_type == "trivia":
            if not number:
                raise ValueError("Missing required parameter 'number' for trivia query")
            url = f"{base_url}/{number}/trivia"
        elif query_type == "math":
            if not number:
                raise ValueError("Missing required parameter 'number' for math query")
            url = f"{base_url}/{number}/math"
        elif query_type == "date":
            if not month or not day:
                raise ValueError("Missing required parameters 'month' and/or 'day' for date query")
            url = f"{base_url}/{month}/{day}/date"
        else:
            raise ValueError(f"Invalid query_type: {query_type}. Must be one of ['trivia', 'math', 'date']")

        # Make API request
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise ValueError(f"API request failed with status code: {response.status_code}")

        # Send the response as output
        agent.send_output(
            agent_output_name='api_response',
            agent_result=response.text
        )

    except Exception as e:
        # Handle and log errors
        agent.send_output(
            agent_output_name='error',
            agent_result=str(e)
        )

def main():
    agent = MofaAgent(agent_name='NumbersAPIIntegrator')
    run(agent=agent)

if __name__ == '__main__':
    main()