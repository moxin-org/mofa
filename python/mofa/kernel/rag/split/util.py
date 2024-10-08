import copy
from pathlib import Path
from typing import List
from langchain_community.document_loaders import Docx2txtLoader, UnstructuredPowerPointLoader, \
    UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import PyPDFLoader
import time
from mofa.utils.files.split import split_txt_by_langchain

from langchain_core.documents import Document

from mofa.utils.string.split import split_str_to_docs
from mofa.utils.variable.util import generate_unique_int

def use_langchain_split_and_gen_ids(loader):
    all_data = []
    pages = loader.load_and_split()
    for doc in pages:
        doc.metadata['id'] = generate_unique_int()
        all_data.append(doc)
    return all_data

def split_docs_page_content(doc,chunk_size:int=328,):
    docs = []
    metadata = copy.deepcopy(doc.metadata)
    if len(doc.page_content) > chunk_size:
        texts = [doc.page_content[i:i + chunk_size] for i in range(0, len(doc.page_content), chunk_size)]
        for text in texts:
            metadata['id'] = generate_unique_int()
            document = Document(
                page_content=text,
                metadata=doc.metadata,
                id=generate_unique_int(),
            )
            docs.append(document)
    return docs

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
                    all_data+= split_docs_page_content(doc=doc,chunk_size=chunk_size)
            elif file_extension == ".doc" or file_extension == ".docx":
                loader = Docx2txtLoader(file_path)
                docs = loader.load_and_split()
                docs_str = ""
                for doc in docs:
                    docs_str += doc.page_content.replace("\n\n\n\n\n\n\n\n","")
                all_data = split_str_to_docs(string=docs_str,chunk_size=chunk_size)
            elif file_extension == ".ppts" or file_extension == ".ppt":
                loader = UnstructuredPowerPointLoader(
                    file_path,
                )
                all_data = use_langchain_split_and_gen_ids(loader)
            elif file_extension == ".md":
                loader = UnstructuredMarkdownLoader(file_path )
                all_data = use_langchain_split_and_gen_ids(loader)
    return all_data
