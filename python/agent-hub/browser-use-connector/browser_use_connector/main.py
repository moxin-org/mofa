from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio

@run_agent
def run(agent:MofaAgent):
    question = agent.receive_parameter('question')
    browser_use_result = asyncio.run(run_browser_use(question))
    agent_output_name = 'agent_result'
    agent.send_output(agent_output_name=agent_output_name,agent_result=browser_use_result)
def main():
    agent = MofaAgent(agent_name='browser-use-connector')
    run(agent=agent)
if __name__ == "__main__":
    main()

async def run_browser_use(question: str):
    agent = Agent(
        task= question,
        llm=ChatOpenAI(model="gpt-4o"),
    )
    return await agent.run()