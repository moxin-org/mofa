from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from langchain_openai import ChatOpenAI

from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv(dotenv_path='.env.secret', override=True)
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL= os.getenv("LLM_BASE_URL")
DEFAULT_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o")

@run_agent
def run(agent:MofaAgent):
    # 接收用户输入的问题
    question = agent.receive_parameter('question')
    # 运行浏览器使用代理并获取历史记录
    history = asyncio.run(run_browser_use(question))
    # 设置代理输出名称
    agent_output_name = 'agent_result'
    # 发送代理结果
    agent.send_output(agent_output_name=agent_output_name,agent_result=history.final_result())

def main():
    # 创建MofaAgent实例
    agent = MofaAgent(agent_name='browser-use-connector')
    # 运行代理
    run(agent=agent)

if __name__ == "__main__":
    # 程序入口
    main()

async def run_browser_use(question: str):
    # 创建Agent实例
    agent = Agent(
        task= question,
        llm=ChatOpenAI(model=DEFAULT_MODEL_NAME, api_key=LLM_API_KEY, base_url=LLM_BASE_URL),
    )
    # 运行Agent并返回结果
    return await agent.run()