# from autogen_group import agent_config_dir_path
from mofa.agent_build.base.base_agent import MofaAgent
import os
from dotenv import load_dotenv
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
async def autogen_group(task: str) -> str:
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    assistant = AssistantAgent("assistant", model_client)
    web_surfer = MultimodalWebSurfer("web_surfer", model_client)
    user_proxy = UserProxyAgent("user_proxy")
    termination = TextMentionTermination("exit")  # Type 'exit' to end the conversation.
    team = RoundRobinGroupChat([web_surfer, assistant, user_proxy], termination_condition=termination)
    result = await Console(team.run_stream(task="Find information about AutoGen and write a short summary."))
    return result
    # agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    # result = await agent.run(task=task)
    # return result

# def main():
#     agent = MofaAgent(agent_name='autogen-agent')
#     while True:
#         load_dotenv(agent_config_dir_path + '/.env')
#         os.environ['OPENAI_API_KEY'] = os.getenv('LLM_API_KEY')
#         result = asyncio.run(autogen_agent(agent.receive_parameter('query')))
#
#         agent.send_output(agent_output_name='autogen_result', agent_result=result.messages[1].content)
if __name__ == "__main__":
    # main()
    os.environ['OPENAI_API_KEY'] =''
    result = asyncio.run(autogen_group('你好'))
    print(result)

