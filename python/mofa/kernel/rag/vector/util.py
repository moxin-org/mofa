import json
import time
from typing import Union, List

from mofa.kernel.rag.split.util import split_files
from mofa.utils.func.util import remove_duplicates_globally


def search_vector(vectorstore, keywords: Union[List[str],str], k: int = 4,**kwargs):
    """
    Search for similar documents in the vector store.

    Parameters:
    vectorstore: PGVector vector store instance.
    keywords (str): Query string.
    k (int, optional): Number of similar documents to return, default is 4.

    Returns:
    similar_docs: List of similar documents.
    """

    data = []
    if isinstance(keywords, str):
        results = vectorstore.similarity_search(keywords, k=k,**kwargs)

        for result in results:
            data.append(result.page_content)
        data = {keywords: list(set(data))}
    elif isinstance(keywords, list):
        data = []
        for keyword in keywords:
            results = vectorstore.similarity_search(keyword, k=k,**kwargs)
            data_values =  [item for d in data for sublist in d.values() for item in sublist]
            results = [item for item in results if item not in data_values]
            data.append({keyword: list(set([i.page_content for i in results]))})

    return remove_duplicates_globally(data)


def upload_files_to_vector(vectorstore, files_path: Union[List[str],str], chunk_size: int = 256, encoding: str = 'utf-8'):
    """
    Upload files to the vector store.

    Parameters:
    vectorstore: PGVector vector store instance.
    files_path (List[str]): List of file paths to upload.
    chunk_size (int, optional): File chunk size, default is 256.
    encoding (str, optional): File encoding format, default is 'utf-8'.

    Returns:
    None.
    """

    t1 = time.time()

    docs = split_files(files_path=files_path, chunk_size=chunk_size, encoding=encoding)
    if len(docs) >= 1:
            if len(docs) > 30:
                for i in range(0, len(docs), 30):
                    batch_docs = docs[i:i + 30]  # 获取当前批次的文档
                    try:
                        batch_ids = [str(doc.metadata["id"]) for doc in batch_docs]
                        vectorstore.add_documents(batch_docs, ids=batch_ids)
                    except Exception as e :
                        batch_ids = [str(doc.id) for doc in batch_docs]
                        vectorstore.add_documents(batch_docs, ids=batch_ids)
            else:
                try:
                    ids = [str(doc.metadata["id"]) for doc in docs]
                    vectorstore.add_documents(docs, ids=ids)
                except Exception as e :
                    ids = [str(doc.id) for doc in docs]
                    vectorstore.add_documents(docs, ids=ids)

    # if len(docs) >=1:
    #     try:
    #         if len(docs)>30:
    #             for i in range(0, len(docs), 30):
    #                 vectorstore.add_documents(docs, ids=[str(doc.metadata["id"]) for doc in docs])
    #     except Exception as e:
    #         vectorstore.add_documents(docs, ids=[str(doc.id) for doc in docs])

    else:
        print(f'{json.dumps(files_path)} Split File Is Empty')
    print('Data To Db  : ', time.time() - t1)
