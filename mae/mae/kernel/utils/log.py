from mae.utils.files.write import write_or_append_to_md_file


def write_agent_log(log_file_path:str=None,log_type:str='md',data:dict=None):
    if log_file_path is not None:
        if log_type == 'markdown' or log_type == 'md':
            write_or_append_to_md_file(data= data,file_path=log_file_path)

