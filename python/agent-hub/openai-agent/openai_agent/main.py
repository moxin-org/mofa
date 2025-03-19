import os
from agents import Agent, Runner

from dotenv import load_dotenv

from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent:MofaAgent):
    query = agent.receive_parameter('query')
    load_dotenv('.env.secret')
    if os.getenv('LLM_API_KEY', None) is not  None:
        os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
    openai_agent = Agent(name="Assistant", instructions="You are a helpful assistant")
    result = Runner.run_sync(openai_agent, query)
    agent.send_output(agent_output_name='openai_agent_result',agent_result=result.final_output)
def main():
    agent = MofaAgent(agent_name='openai-agent')
    run(agent=agent)
if __name__ == "__main__":
    main()



