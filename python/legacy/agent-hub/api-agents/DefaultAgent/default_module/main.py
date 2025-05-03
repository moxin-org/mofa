from mofa.agent_build.base.base_agent import MofaAgent, run_agent

@run_agent
def run(agent: MofaAgent):
    try:
        # Input handling - Example for receiving a single parameter
        input_param = agent.receive_parameter('input_port')

        # Core logic - Example business logic (echo the input)
        processed_data = f"Processed: {input_param}"

        # Output delivery
        agent.send_output(
            agent_output_name='output_port',
            agent_result=processed_data  # Ensure serialization
        )
    except Exception as e:
        # Handle errors within Agent boundaries
        agent.send_output(
            agent_output_name='error_port',
            agent_result=f"Error: {str(e)}"
        )

def main():
    agent = MofaAgent(agent_name='DefaultAgent')
    run(agent=agent)

if __name__ == '__main__':
    main()