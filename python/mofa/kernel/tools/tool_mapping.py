from typing import List, Union
from mofa.kernel.tools.util import stock_data,  text_rag
from mofa.kernel.tools.vector import delete_vector_collection_with_tool,upload_files_to_vector_with_tool,search_vector_with_tool


from mofa.kernel.rag.embedding.huggingface import load_embedding_model
from mofa.utils.date.util import now_time
# from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from crewai_tools import TXTSearchTool

from mofa.utils.download.arxiv_papers import arxiv_search_and_download
from mofa.utils.files.dir import delete_all_files_in_folder
from mofa.utils.files.read import read_excel
# from langchain.tools import DuckDuckGoSearchRun

from mofa.utils.files.read import read_excel




def get_tool_func(func_name:str):
    # tool_mapping = {'now_time':now_time,'stock_data':stock_data,'DuckDuckGoSearchRun':DuckDuckGoSearchRun,'text_rag':text_rag,'whisper_translate_audio':whisper_translate_audio,'TXTSearchTool':TXTSearchTool(),'PDFSearchTool':PDFSearchTool(),'read_excel':read_excel,'create_pgvector':create_pgvector,'delete_vector_collection':delete_vector_collection,'upload_files_to_vector':upload_files_to_vector,"search_vector":search_vector,"load_embedding_model":load_embedding_model}
    tool_mapping = {'now_time':now_time,'stock_data':stock_data,'text_rag':text_rag,'read_excel':read_excel,'delete_vector_collection_with_tool':delete_vector_collection_with_tool,'upload_files_to_vector_with_tool':upload_files_to_vector_with_tool,'search_vector_with_tool':search_vector_with_tool,'TXTSearchTool':TXTSearchTool(),'arxiv_search_and_download':arxiv_search_and_download,'delete_all_files_in_folder':delete_all_files_in_folder}
    # tool_mapping = {'now_time':now_time,'stock_data':stock_data,'text_rag':text_rag,'whisper_translate_audio':whisper_translate_audio,'read_excel':read_excel,}
    return tool_mapping.get(func_name,None)

def agent_tools(tool_names:Union[List[str],None]=None):
    if tool_names is None:
        return []
    tools = []
    for tool_name in tool_names:
        # tool_func = tool_mapping.get(tool_name, None)
        tool_func = get_tool_func(func_name=tool_name)
        if tool_func is not None:
            tools.append(tool_func)
    return tools
