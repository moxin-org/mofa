from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import requests

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling
        word = agent.receive_parameter('word')

        # Core logic: Query the dictionary API
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        if response.ok:
            definition = response.json()[0]["meanings"][0]["definitions"][0]["definition"]
            processed_data = f"{word}: {definition}"
        else:
            processed_data = "未找到释义"

        # Output delivery
        agent.send_output(
            agent_output_name='definition_result',
            agent_result=processed_data
        )
    except Exception as e:
        # Error handling
        agent.send_output(
            agent_output_name='error',
            agent_result=f"An error occurred: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='WordDefinitionAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()