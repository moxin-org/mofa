
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mofa.utils.files.read import read_yaml
from deepseek import agent_config_dir_path

@run_agent
def run(agent: MofaAgent):
    # Load environment variables
    load_dotenv(os.path.join(agent_config_dir_path, '.env.secret'))

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv('LLM_API_KEY'), base_url="https://api.deepseek.com")

    # Prepare the prompt
    prompt = read_yaml(file_path=os.path.join(agent_config_dir_path, 'configs', 'agent.yml')).get('agent', {}).get('prompt', '')

    # Receive the user query and search data
    user_query = agent.receive_parameter('query')

    # Create the messages for the chat completion
    messages = [
        {"role": "system", "content": json.dumps(prompt)},
        {"role": "user", "content": f"user q: {user_query}  "}
    ]

    # Get the response from the OpenAI API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
    )

    # Send the response back to the agent
    agent.send_output(agent_output_name='create_agent_main_result', agent_result=response.choices[0].message.content)

def main():
    agent = MofaAgent(agent_name='create_agent_main')
    run(agent=agent)

if __name__ == "__main__":
    main()
