import os

import yaml

import os
import shutil
def dict_to_md(data, level=1):
    md = ""
    for key, value in data.items():
        md += f"{'#' * level} {key}\n\n"
        if isinstance(value, dict):
            md += dict_to_md(value, level + 1)
        else:
            md += f"{value}\n\n"
    return md

def ensure_directory_exists(file_path:str):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_or_append_to_md_file(data:dict, file_path:str="data.md"):
    ensure_directory_exists(file_path=file_path)
    if os.path.exists(file_path):
        mode = "a"
    else:
        mode = "w"

    with open(file_path, mode) as f:
        md_content = dict_to_md(data)
        f.write(md_content)

def write_dict_to_yml(data:dict, file_path:str=".data.yml"):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)




def copy_file(input_file='.env.secret', output_file='.env', overwrite=False):
    try:
        # 检查输入文件是否存在
        if os.path.exists(input_file):
            # 检查输出文件是否存在
            if os.path.exists(output_file):
                if overwrite:
                    shutil.copy(input_file, output_file)
                    print(f"File '{input_file}' overwritten successfully as '{output_file}'.")
                else:
                    print(f"Output file '{output_file}' already exists. Not overwriting.")
            else:
                shutil.copy(input_file, output_file)
                print(f"File '{input_file}' copied successfully to '{output_file}'.")
        else:
            print(f"Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")