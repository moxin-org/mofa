from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    # Input handling
    operation = agent.receive_parameter('operation')
    expression = agent.receive_parameter('expression')

    # Validate operation
    valid_operations = ['derive', 'integrate', 'zeroes']
    if operation not in valid_operations:
        agent.send_output('error', f"Invalid operation. Valid operations are: {valid_operations}")
        return

    # Construct API URL
    url = f"https://newton.now.sh/api/v2/{operation}/{expression}"

    try:
        # Make API request
        response = requests.get(url)
        response.raise_for_status()

        # Process response
        data = response.json()
        agent.send_output('result', {
            'expression': data['expression'],
            'result': data['result']
        })

    except requests.exceptions.RequestException as e:
        agent.send_output('error', f"API request failed: {str(e)}")
    except ValueError as e:
        agent.send_output('error', f"Invalid API response: {str(e)}")

def main():
    agent = MofaAgent(agent_name='NewtonMathAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()