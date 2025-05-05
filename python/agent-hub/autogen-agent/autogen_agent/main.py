import json

from autogen_agent import agent_config_dir_path
from mofa.agent_build.base.base_agent import MofaAgent, run_agent
import os
from dotenv import load_dotenv
from openai import OpenAI
from mofa.utils.files.read import read_yaml
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

async def autogen_agent(task: str) -> str:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    result = await agent.run(task=task)
    return result

    
@run_agent
def run(agent: MofaAgent):
    os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
    result = asyncio.run(autogen_agent(agent.receive_parameter('query')))

    agent.send_output(agent_output_name='autogen_result', agent_result=result.messages[1].content)
def main():
    # 创建MofaAgent实例
    agent = MofaAgent(agent_name='autogen-agent')
    # 运行代理
    run(agent=agent)

if __name__ == "__main__":
    main()

