from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        input_param = agent.receive_parameter('query')
        operation = agent.receive_parameter('operation')  # 'random', 'by_id', or 'search'

        # Core logic
        if operation == 'random':
            url = "https://api.adviceslip.com/advice"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                processed_data = {
                    "advice_id": data['slip']['id'],
                    "advice_text": data['slip']['advice']
                }
            else:
                processed_data = {"error": f"Request failed with status code: {response.status_code}"}

        elif operation == 'by_id':
            slip_id = input_param
            url = f"https://api.adviceslip.com/advice/{slip_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                processed_data = {
                    "advice_id": data['slip']['slip_id'],
                    "advice_text": data['slip']['advice']
                }
            else:
                processed_data = {"error": f"Request failed with status code: {response.status_code}"}

        elif operation == 'search':
            query = input_param
            url = f"https://api.adviceslip.com/advice/search/{query}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                processed_data = {
                    "total_results": data['total_results'],
                    "results": [slip['advice'] for slip in data['slips']]
                }
            else:
                processed_data = {"error": f"Request failed with status code: {response.status_code}"}

        else:
            processed_data = {"error": "Invalid operation. Choose 'random', 'by_id', or 'search'."}

        # Output delivery
        agent.send_output(
            agent_output_name='api_response',
            agent_result=processed_data
        )

    except Exception as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={"error": str(e)}
        )

def main():
    agent = MofaAgent(agent_name='AdviceSlipAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()