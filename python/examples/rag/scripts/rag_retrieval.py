import os

from langchain_openai import OpenAIEmbeddings
from pathlib import Path

from mofa.agent_build.base.llm_client import init_dspy_llm_client
from mofa.agent_build.reasoner.reasoner import ReasonerRagModule
from mofa.utils.files.read import read_yaml
from mofa.utils.files.util import get_all_files

# os.environ["OPENAI_API_KEY"] = "  "
# os.environ["OPENAI_API_BASE"] = "https://api.siliconflow.cn/v1"
# model_name = "BAAI/bge-large-zh-v1.5"
# embedding = OpenAIEmbeddings(model=model_name)
#
# input_text = "The meaning of life is 42"
# vector = embedding.embed_query(input_text)
# print(vector[:3])


import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


# yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='rag_retrieval.yml')
# inputs = {k.lower():v  for k,v in read_yaml(yaml_file_path).get("RAG").items()}
# task = "Who are the authors of the paper? How long did it take to create it? "
# os.environ["OPENAI_API_KEY"] = inputs.get("rag_model_api_key")
# os.environ["OPENAI_API_BASE"] =  inputs.get("rag_model_api_url")
# agent_result = []
# init_dspy_llm_client({k.lower():v  for k,v in read_yaml(yaml_file_path).get("MODEL").items()})
# for files_path in inputs.get('files_path'):
#     if Path(files_path).is_dir():
#         for file_path in get_all_files(files_path):
#             collection_name = Path(file_path).name
#             rag_module = ReasonerRagModule(module_path=inputs.get("module_path"),model_name=inputs.get("rag_model_name"),  collection_name=collection_name, is_upload_file=inputs.get("is_upload_file"), files_path=[file_path],encoding=inputs.get("encoding"),chunk_size=inputs.get('chunk_size'),multi_process=False,rag_search_num=inputs.get("rag_search_num"),temperature=0.7,chroma_path=inputs.get("chroma_path"))
#             agent_result += rag_module.rag_retrieval(question=task)
#     else:
#         collection_name = Path(files_path).name
#         rag_module = ReasonerRagModule(module_path=inputs.get("module_path"),model_name=inputs.get("rag_model_name"),  collection_name=collection_name, is_upload_file=inputs.get("is_upload_file"), files_path=[files_path],encoding=inputs.get("encoding"),chunk_size=inputs.get('chunk_size'),multi_process=False,rag_search_num=inputs.get("rag_search_num"),temperature=0.7,chroma_path=inputs.get("chroma_path"))
#         agent_result += rag_module.rag_retrieval(question=task)
# print(agent_result)
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
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='rag_retrieval.yml')
                inputs = {k.lower():v  for k,v in read_yaml(yaml_file_path).get("RAG").items()}
                os.environ["OPENAI_API_KEY"] = inputs.get("rag_model_api_key")
                os.environ["OPENAI_API_BASE"] =  inputs.get("rag_model_api_url")
                agent_result = []
                init_dspy_llm_client({k.lower():v  for k,v in read_yaml(yaml_file_path).get("MODEL").items()})
                for files_path in inputs.get('files_path'):
                    if Path(files_path).is_dir():
                        for file_path in get_all_files(files_path):
                            collection_name = Path(file_path).name
                            rag_module = ReasonerRagModule(module_path=inputs.get("module_path"),model_name=inputs.get("rag_model_name"),  collection_name=collection_name, is_upload_file=inputs.get("is_upload_file"), files_path=[file_path],encoding=inputs.get("encoding"),chunk_size=inputs.get('chunk_size'),multi_process=False,rag_search_num=inputs.get("rag_search_num"),temperature=0.7,chroma_path=inputs.get("chroma_path"))
                            agent_result += rag_module.rag_retrieval(question=task)
                    else:
                        collection_name = Path(files_path).name
                        rag_module = ReasonerRagModule(module_path=inputs.get("module_path"),model_name=inputs.get("rag_model_name"),  collection_name=collection_name, is_upload_file=inputs.get("is_upload_file"), files_path=[files_path],encoding=inputs.get("encoding"),chunk_size=inputs.get('chunk_size'),multi_process=False,rag_search_num=inputs.get("rag_search_num"),temperature=0.7,chroma_path=inputs.get("chroma_path"))
                        agent_result += rag_module.rag_retrieval(question=task)
                send_output("context_rag", pa.array([create_agent_output(step_name='context_rag',
                                                                              output_data=agent_result,
                                                                              dataflow_status=os.getenv(
                                                                                  'IS_DATAFLOW_END', False))]),
                            dora_event['metadata'])

        return DoraStatus.CONTINUE