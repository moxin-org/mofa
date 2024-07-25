from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
import time
from mae.utils.files.split import split_txt_by_langchain

from langchain_core.documents import Document

from mae.utils.variable.util import generate_unique_int


def split_files(files_path: List[str], chunk_size: int = 256, encoding: str = 'utf-8'):
    """
    Split the files from the given list of file paths into chunks and return a list of documents containing the split text.

    Parameters:
    files_path (List[str]): List of file paths.
    chunk_size (int, optional): Size of each text chunk, default is 256.
    encoding (str, optional): Encoding format of the files, default is 'utf-8'.

    Returns:
    all_data (List[Document]): List of documents containing the split text chunks, each document includes text content and metadata.
    """

    all_data = []
    id_num = 0
    for num, file_path in enumerate(files_path):
        file_path = Path(file_path)
        if file_path.is_file():
            file_extension = file_path.suffix
            if file_extension == '.txt':
                data = split_txt_by_langchain(chunk_size=chunk_size, file_path=str(file_path), encoding=encoding)
                if len(data) > 0:
                    for num, text in enumerate(data):
                        id_num += 1
                        doc = Document(page_content=text,
                                       metadata={"id": id_num, 'chunk_index': num, 'chunk_size': len(text),
                                                 'source': file_path})
                        all_data.append(doc)
            elif file_extension == '.pdf':
                loader = PyPDFLoader(str(file_path))
                pages = loader.load_and_split()
                for doc in pages:
                    id_num += 1
                    doc.metadata['id'] = generate_unique_int()
                    all_data.append(doc)
    return all_data
