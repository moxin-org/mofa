import os
from pathlib import Path
from typing import Union, Generator


def get_all_files(dir_path: Union[str, Path], file_type: Union[str, None] = None) -> Generator:
    for root, ds, fs in os.walk(dir_path):
        for f in fs:
            fullname = os.path.join(root, f)
            if file_type is not None:
                if isinstance(file_type, str):
                    file_type = [file_type]
            if '.' == Path(fullname).name[0] or (
                file_type is not None and (Path(fullname).suffix.replace('.', '') not in file_type)):
                continue

            yield fullname

def create_file_dir(file_path:str):
    db_dir = os.path.dirname(file_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)