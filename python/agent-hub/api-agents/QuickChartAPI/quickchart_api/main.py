from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests
import json

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive input parameters
        input_params = agent.receive_parameters(['chart_config', 'qr_data'])
        
        # Process chart generation if chart_config is provided
        if 'chart_config' in input_params and input_params['chart_config']:
            chart_config = json.loads(input_params['chart_config'])
            params = {
                "c": chart_config,
                "width": 500,
                "height": 300
            }
            response = requests.get("https://quickchart.io/chart", params=params)
            if response.status_code == 200:
                agent.send_output('chart_image', response.content)
            else:
                agent.send_output('error', f"Chart request failed with status code: {response.status_code}")
        
        # Process QR code generation if qr_data is provided
        if 'qr_data' in input_params and input_params['qr_data']:
            qr_params = {
                "text": input_params['qr_data'],
                "size": 300,
                "foregroundColor": "navy",
                "backgroundColor": "white",
                "ecLevel": "H"
            }
            response = requests.get("https://quickchart.io/qr", params=qr_params)
            if response.status_code == 200:
                agent.send_output('qr_image', response.content)
            else:
                agent.send_output('error', f"QR code request failed with status code: {response.status_code}")
    except Exception as e:
        agent.send_output('error', f"An error occurred: {str(e)}")

def main():
    agent = MofaAgent(agent_name='QuickChartAPI')
    run(agent=agent)

if __name__ == '__main__':
    main()