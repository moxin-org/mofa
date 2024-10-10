import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
import re
from mofa.kernel.utils.util import load_agent_config, create_agent_output
from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data', 'task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()

                yaml_file_path = get_relative_path(
                    current_file=__file__,
                    sibling_directory_name='configs',
                    target_file_name='planning_agent.yml'
                )
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task

                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                # print("agent_result: ", agent_result)
                
                raw_result = self.extract_json_from_text(agent_result)
                # print("raw_result", raw_result)

                processed_result = self.process_llm_output(raw_result)
                # print('processed_result:', processed_result)

                record_agent_result_log(
                    agent_config=inputs,
                    agent_result={
                        "1, " + inputs.get('log_step_name', "Step_one"): {task: processed_result}
                    }
                )

                send_output(
                    "planning_results",
                    pa.array([create_agent_output(
                        step_name='keyword_results',
                        output_data=processed_result,
                        dataflow_status=os.getenv('IS_DATAFLOW_END', True)
                    )]),
                    dora_event['metadata']
                )
                print('planning_results:', processed_result)

        return DoraStatus.CONTINUE

    def extract_json_from_text(self,raw_input):
        try:
            json_match = re.search(r'\{.*\}', raw_input, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
                result_data = json.loads(json_content)
                return result_data
            else:
                print("No JSON structure found in input.")
                return {"error": "No JSON found"}

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {"error": "Invalid JSON structure"}

    # return small tasks in json format
    # def process_llm_output(self, agent_result):
    #     try:
    #         if isinstance(agent_result, dict):
    #             result_data = agent_result
    #         else:
    #             result_data = json.loads(agent_result)
            
    #         if 'tasks' in result_data:
    #             for task in result_data['tasks']:
    #                 if 'task_id' in task:
    #                     task['task_id'] = str(task['task_id'])
            
    #         tasks = result_data.get('tasks', [])
            
    #         processed_tasks = []
    #         for task in tasks:
    #             task_info = {
    #                 "task_id": task.get("task_id"),
    #                 "description": task.get("description"),
    #                 "classification": task.get("classification"),
    #                 "is_synchronous": task.get("is_synchronous"),
    #                 "dependencies": task.get("dependencies", [])
    #             }
    #             processed_tasks.append(task_info)
            
    #         return processed_tasks
        
    #     except json.JSONDecodeError as e:
    #         print(f"Error decoding LLM result: {e}")
    #         return {"error": "Invalid LLM response"}
    #     except Exception as e:
    #         print(f"Unexpected error processing LLM result: {e}")
    #         return {"error": f"Unexpected error: {str(e)}"}
    
    
    # return small tasks in a more readable way
    def process_llm_output(self, agent_result):
        try:
            if isinstance(agent_result, str):
                result_data = json.loads(agent_result)
            else:
                result_data = agent_result
            
            tasks = result_data.get('tasks', [])
            
            valid_tasks = [
                task for task in tasks 
                if task.get("task_id") is not None and task.get("description") is not None
            ]

            if not valid_tasks:
                return {"error": "No valid tasks found in the response"}

            formatted_tasks = []
            for task in valid_tasks:
                task_info = (
                    f"Task ID: {task['task_id']}\n"
                    f"Description: {task['description']}\n"
                    f"Type: {'Synchronous' if task['is_synchronous'] else 'Asynchronous'}\n"
                    f"Dependencies: {', '.join(task['dependencies']) if task['dependencies'] else 'None'}\n"
                )
                formatted_tasks.append(task_info)
            
            return "\n".join(formatted_tasks)
        
        except json.JSONDecodeError as e:
            print(f"Error decoding LLM result: {e}")
            return {"error": "Invalid LLM response"}
