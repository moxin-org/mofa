from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent:MofaAgent):
    task = agent.receive_parameter('task')

    # TODO: 在下面添加你的Agent代码,其中agent_inputs是你的Agent的需要输入的参数
    # reasoner = ReasonerAgent(config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/configs/config.yml',
    #                     llm_config_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), ) + '/.env.secret')
    # result = reasoner.run(**agent.agent_inputs)
    # print('reasoner_result : ',result)
    agent_output_name = 'agent_result'
    agent.send_output(agent_output_name=agent_output_name,agent_result=task)
def main():
    agent = MofaAgent(agent_name='you-agent-name')
    run(agent=agent)
if __name__ == "__main__":
    main()
