import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.utils.log.agent import record_agent_result_log

class Operator:
    def __init__(self):
        self.answer_1 = None
        self.answer_2 = None
        self.task = None

    def on_event(self, dora_event, send_output) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] == "answer_1_response":
                self.answer_1 = dora_event["value"][0].as_py()
                #print('Received Answer 1:', self.answer_1)
            elif dora_event["id"] == "answer_2_response":
                self.answer_2 = dora_event["value"][0].as_py()
                #print('Received Answer 2:', self.answer_2)
            elif dora_event["id"] == "task":
                self.task = dora_event["value"][0].as_py()
                #print('Received Task:', self.task) 

            if self.answer_1 and self.answer_2 and self.task:
                yaml_file_path = yaml_file_path = '/home/mofaDora/mofa/python/examples/agentfight1/configs/judge_agent.yml'

                inputs = load_agent_config(yaml_file_path)
                # inputs["task"] = self.task
                # inputs["answer_1"] = self.answer_1
                # inputs["answer_2"] = self.answer_2

                inputs['input_fields'] = {'answer_1_response': self.answer_1,'answer_2_response':self.answer_2,'task':self.task}

                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                #print('1')

                record_agent_result_log(agent_config=inputs, agent_result={"Evaluation": agent_result})
                #print('2')

                send_output("evaluation_result", pa.array([create_agent_output(agent_name='evaluation_result', agent_result=agent_result, dataflow_status=os.getenv('IS_DATAFLOW_END', True))]), dora_event['metadata'])
                #print('3')

                print('Received Answer 1:', self.answer_1)
                print('Received Answer 2:', self.answer_2)
                print('Evaluation Result:', agent_result)

                self.answer_1 = None
                self.answer_2 = None
                self.task = None

        return DoraStatus.CONTINUE
