from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from openai import OpenAI
import os
from dotenv import load_dotenv

@run_agent
def run(agent: MofaAgent):
    user_input = agent.receive_parameter('query')

    # 加载 .env 文件
        # dotenv_loaded = load_dotenv('.env.secret', override=True)

        # client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")
        # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key='sk-79af9650eba046a9871245d2bd625918',
        base_url='https://api.deepseek.com/v1'
    )

    # 接收用户输入

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False)

    # 发送输出
    agent.send_output(
        agent_output_name='robot_agent_result',
        agent_result=str(response.choices[0].message.content)
    )
      

def main():
    agent = MofaAgent(agent_name='robot-agent')
    run(agent=agent)

if __name__ == "__main__":
    main()


