import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log

from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool

from calculator.tool import calculator, calculator_2, newton_calculator

# Define a dictionary to map function names to actual callables
available_functions = {
    'calculator': calculator,
    'calculator_2': calculator_2,
    'newton_calculator': newton_calculator,
}

class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='tools_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task
                # agent_result = run_dspy_or_crewai_agent(agent_config=inputs)

                # Initialize an LLM (example using OpenAI)
                os.environ["OPENAI_API_KEY"] = inputs.get('model_api_key')
                llm = OpenAI(temperature=0,model=inputs.get('model_name'),openai_api_key=inputs.get('model_api_key'),base_url=inputs.get("model_api_url"))

                # Create tools list (in this case, only the calculator tool)
                function_name = inputs.get('tool_func', "calculator")
                tools = [
                    Tool(
                        name=inputs.get('tool_name', "Calculator"),
                        func=available_functions[function_name],
                        description=inputs.get('tool_description', "Useful for performing arithmetic calculations. Input should be a valid arithmetic expression like '2 + 2' or '10 / 2'.")
                    )
                ]

                # Initialize an agent with the LLM and tools
                agent = initialize_agent(
                    tools, llm, agent_type="reasoner", verbose=True
                )

                agent_result = agent.run(task)

                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): {task:agent_result}})
                send_output("reasoner_results", pa.array([create_agent_output(step_name='keyword_results', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print('reasoner_results:', agent_result)

        return DoraStatus.CONTINUE