from typing import Dict, Any, List

from attr import define

from mae.utils.files.dir import copy_directories
from mae.utils.files.read import read_yaml, modify_agents_inputs
import attrs
from attrs import define,field

from mae.utils.files.util import find_file, get_file_name
from mae.utils.files.write import write_dict_to_yml


@define
class MergeDataflow:
    def get_node_id_data(self,dataflow:dict,node_id:str):

        # 获取节点列表
        nodes = dataflow.get("nodes", [])

        # 遍历节点列表，查找匹配的节点 ID
        for node in nodes:
            if node.get("id") == node_id:
                return node

        # 如果未找到匹配的节点 ID，返回 None
        return None

    def list_node_ids(self,dataflow:dict):
        return [i.get('id') for i in dataflow.get('nodes')]
    def get_dataflow_dynamic_node_ids(self,dataflow:dict)->list[str]:
        nodes = dataflow.get("nodes", [])
        dynamic_node_ids = []
        for node in nodes:
            if node.get('path',None) == 'dynamic':
                dynamic_node_ids.append(node.get('id'))
        return dynamic_node_ids
    def get_node_id_outputs(self,dataflow:dict,node_id:str,):
        node = self.get_node_id_data(dataflow, node_id)

        # 如果节点存在，返回其输出
        if node:
            return node.get("outputs", None)
        # 如果节点不存在，返回 None
        return None
    def get_second_node_name(self,dataflow:dict):
        return self.list_node_ids(dataflow=dataflow)[1]

    def delete_nodes_and_associated_links(self,dataflow: Dict[str, Any], node_ids_to_delete: List[str]) -> Dict[str, Any]:
        # Step 1: Find the outputs associated with the nodes to delete
        outputs_to_delete = set()
        for node in dataflow['nodes']:
            if node['id'] in node_ids_to_delete:
                if 'outputs' in node:
                    for output in node['outputs']:
                        outputs_to_delete.add(f"{node['id']}/{output}")

        # Step 2: Remove the nodes themselves
        dataflow['nodes'] = [node for node in dataflow['nodes'] if node['id'] not in node_ids_to_delete]

        # Step 3: Remove the associated inputs in other nodes
        for node in dataflow['nodes']:
            if 'operator' in node:
                if 'inputs' in node['operator']:
                    inputs_to_delete = [key for key, value in node['operator']['inputs'].items() if value in outputs_to_delete]
                    for input_key in inputs_to_delete:
                        del node['operator']['inputs'][input_key]

        return dataflow
    def add_node_inputs(self,dataflow:dict,node_id:str,target_node_inputs:list[dict]):
        node_data = self.get_node_id_data(dataflow=dataflow, node_id=node_id)
        node_inputs = node_data.get('operator').get('inputs')
        new_node_inputs = {f"{target_node_input.get('output_params_name')}": f"{target_node_input.get('output_node_id')}/{target_node_input.get('output_params_name')}" for target_node_input in target_node_inputs}
        node_inputs.update(new_node_inputs)
        node_data['operator']['inputs'] = node_inputs
        return dataflow

    def merge_dataflow_with_yml(self, left_dataflow:dict,right_dataflow:dict,dependencies:dict):
        right_dataflow = self.add_node_inputs(dataflow=right_dataflow, node_id=dependencies.get('target_node_id'), target_node_inputs=dependencies.get('target_node_inputs'))
        left_dataflow['nodes']+=right_dataflow.get('nodes')
        # write_dict_to_yml(data=left_dataflow,file_path=yml_file)
        return left_dataflow

    def add_inputs_by_agent_file(self, dataflow:dict,input_node_id:str,output_dir_path:str,new_agents_inputs:list[str],search_directory:str):
        node_data = self.get_node_id_data(dataflow=dataflow,node_id=input_node_id)
        node_py_file_name = node_data.get('operator').get('python').split('/')[-1]
        find_run_py_file = find_file(target_filename=node_py_file_name,search_directory=search_directory)
        output_file_path = f"{output_dir_path}/{node_data.get('operator').get('python')[1:]}"
        modify_agents_inputs(file_path=find_run_py_file,new_inputs=new_agents_inputs,output_file_path=output_file_path)

    def generate_agents(self,left_agents_yml:str,right_agents_yml:str,dependencies:list[dict],output_dir_path:str,search_directory:str):
        left_agents_config = read_yaml(left_agents_yml)
        right_agents_config = read_yaml(right_agents_yml)
        for dependency in dependencies:
            left_agents_config = self.merge_dataflow_with_yml(left_dataflow=left_agents_config, right_dataflow=right_agents_config, dependencies=dependency)
            right_dataflow_dynamic_node_ids = self.get_dataflow_dynamic_node_ids(dataflow=right_agents_config)
            left_agents_config = self.delete_nodes_and_associated_links(dataflow=left_agents_config, node_ids_to_delete=right_dataflow_dynamic_node_ids)
            self.add_inputs_by_agent_file(dataflow=right_agents_config,output_dir_path=output_dir_path,input_node_id=dependency.get('target_node_id'),new_agents_inputs=[dependency.get('target_node_inputs')[0].get('output_params_name')],search_directory=search_directory)
        write_dict_to_yml(data=left_agents_config, file_path=f"{output_dir_path}/{get_file_name(file_path=left_agents_yml)}")
        return left_agents_config




    def copy_agents_files(self,agents_dir_path:str,agents_name:list[str],output_dir_path:str,subdirectories:list[str]=['scripts','configs']):
        for agent_name in agents_name:
            source_dir_path = f"{agents_dir_path}/{agent_name}"
            copy_directories(source_directory=source_dir_path,
                             subdirectories=subdirectories,destination_directory=f"{output_dir_path}")


# web_search_yml_file_path = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/web_search/web_search_dataflow.yml'
# reasoner_yml_file_path = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/reasoner/reasoner_dataflow.yml'
# output_dir_path='/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/examples/generate'
# search_directory = '/Users/chenzi/project/zcbc/Moxin-App-Engine/mae/mae/agent_link/agent_template'
# agents_name = ['web_search','reasoner']
# reasoner_config,web_search_config = read_yaml(reasoner_yml_file_path),read_yaml(web_search_yml_file_path)
# dependencies = [{'source_node_id': ['more_question_agent'], 'target_node_id': 'reasoner_agent', 'target_node_inputs': [{'output_node_id': 'more_question_agent', 'output_params_name': 'more_question_results'}]}]
# merge_dataflow = MergeDataflow()
# merge_dataflow.copy_agents_files(agents_dir_path=search_directory,agents_name=agents_name,output_dir_path=output_dir_path,subdirectories=['scripts','configs'])
# dataflow = merge_dataflow.generate_agents(output_dir_path=output_dir_path,
#                                           left_agents_yml=web_search_yml_file_path,
#                                           right_agents_yml=reasoner_yml_file_path,
#                                           dependencies=dependencies,search_directory=search_directory)
# print(dataflow)