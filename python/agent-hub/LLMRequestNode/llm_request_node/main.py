from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
import openai

@run_agent
def run(agent: MofaAgent):
    try:
        # Receive the input query from another node
        query = agent.receive_parameter('query')

        # Get API key from environment
        api_key = os.getenv('LLM_API_KEY')
        if not api_key:
            raise ValueError('LLM_API_KEY environment variable is not set.')

        # Initialize OpenAI client (replace as needed for other LLMs)
        openai.api_key = api_key

        # Call OpenAI Chat API (can adapt model as needed)
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': query}]
        )
        llm_content = response['choices'][0]['message']['content']
        
        # Send output through agent port
        agent.send_output(
            agent_output_name='llm_response',
            agent_result=llm_content
        )
    except Exception as e:
        # Error handling with string serialization
        agent.send_output(
            agent_output_name='llm_response',
            agent_result=f'Error: {str(e)}'
        )

def main():
    agent = MofaAgent(agent_name='LLMRequestNode')
    run(agent=agent)

if __name__ == '__main__':
    main()
