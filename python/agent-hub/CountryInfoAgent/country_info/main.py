from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        country_name = agent.receive_parameter('country_name')
        
        # API call
        response = requests.get(f"https://restcountries.com/v3.1/name/{country_name}")
        response.raise_for_status()
        country_data = response.json()[0]
        
        # Extract information
        capital = country_data['capital'][0]
        currency = list(country_data['currencies'].keys())[0]
        
        # Prepare output
        result = {
            'capital': capital,
            'currency': currency
        }
        
        # Output delivery
        agent.send_output(
            agent_output_name='country_info',
            agent_result=result
        )
    except requests.exceptions.RequestException as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': str(e)}
        )
    except (KeyError, IndexError) as e:
        agent.send_output(
            agent_output_name='error',
            agent_result={'error': f'Invalid data format: {str(e)}'}
        )

def main():
    agent = MofaAgent(agent_name='CountryInfoAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()