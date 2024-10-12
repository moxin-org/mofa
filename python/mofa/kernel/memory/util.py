import os

from mem0 import Memory

from mofa.utils.files.read import read_yaml




def load_mem0_client(file_path:str):
    mem0_config = read_yaml(file_path).get('config')
    model_config = read_yaml(file_path).get("model")
    if model_config.get('model_api_url',None) is not None:
        os.environ["OPENAI_API_BASE"] = model_config.get('model_api_url')
    os.environ["OPENAI_API_KEY"] = model_config.get('model_api_key')
    m = Memory.from_config(mem0_config)
    return m

def load_user_id(file_path:str):
    return read_yaml(file_path).get("user_id")

def get_mem0_search_text(memory_datas):
    try:
        results = list(set([memory_data.get("memory") for memory_data in memory_datas]))
    except Exception as e :
        results = memory_datas.get("results")
    return results