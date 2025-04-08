from mofa.agent_build.base.base_agent import MofaAgent, run_agent
from mcp.server.fastmcp import FastMCP

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@run_agent
def run(agent:MofaAgent):
    task = agent.receive_parameter('task')
    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    agent_output_name = 'agent_result'
    agent.send_output(agent_output_name=agent_output_name,agent_result=task)
def main():
    agent_name = 'Mofa-Mcp'
    agent = MofaAgent(agent_name=agent_name)
    run(agent=agent)

if __name__ == "__main__":
    main()
