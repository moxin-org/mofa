from mofa.agent_build.base.base_agent import MofaAgent, run_agent

def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * add(a,b)


@run_agent
def run(agent):
    agent.register_mcp_tool(add)
    agent.register_mcp_tool(multiply)
    print('开始运行mcp服务')
    agent.run_mcp()
    agent.receive_parameter('query')

def main():
    agent_name = 'Mofa-Mcp'
    agent = MofaAgent(agent_name=agent_name)
    run(agent)

if __name__ == "__main__":
    main()
