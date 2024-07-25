import shutil
from pathlib import Path
from typing import Union
import os

def check_dir(dir_path: Union[Path, str]):
    # Convert the input to a Path object if it's not already
    folder_path = Path(dir_path)
    # Return True if the folder exists, otherwise False
    return folder_path.exists() and folder_path.is_dir()


def make_dir(dir_path: Union[Path, str]):
    p: Path = Path(dir_path)
    p.mkdir(exist_ok=True, parents=True)


def remove_dir(dir_path: Union[str, Path]):
    if Path(dir_path).is_dir():
        shutil.rmtree(dir_path)



def delete_all_files_in_folder(folder_path:str):
    """
    Delete all files and subfolders in the specified folder.

    Parameters:
    folder_path (str): Path to the folder whose contents are to be deleted.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


