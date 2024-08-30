from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_openai import OpenAIEmbeddings
def load_embedding_model(module_path:str=None,model_name:str=None,multi_process:bool=False,model_kwargs:dict={'device':0}):
    """
    Load an embedding model, selecting different embedding implementations based on the provided path or model name.

    Parameters:
    module_path (str, optional): Path to the HuggingFace model.
    model_name (str, optional): Name of the OpenAI model.
    multi_process (bool, optional): Whether to enable multi-processing, default is False.
    model_kwargs (dict, optional): Additional parameters for model initialization, default is {'device': 0}, specifying the device.

    Returns:
    embedding: Loaded embedding model instance, using HuggingFace or OpenAI implementation based on the provided parameters.
    """

    embedding = None
    if module_path is not None:
        try:
            embedding = HuggingFaceEmbeddings(model_name=module_path, model_kwargs=model_kwargs, show_progress=True,multi_process=multi_process, )
        except Exception as e :
            embedding = HuggingFaceEmbeddings(model_name=module_path, model_kwargs={'device': 'cpu'}, show_progress=True, multi_process=multi_process, )
    elif model_name is not None and module_path is None:
        embedding = OpenAIEmbeddings(model=model_name)
    return embedding
