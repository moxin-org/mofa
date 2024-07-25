import json
from typing import List, Union
import time
from langchain_postgres import PGVector

from mae.kernel.rag.split.util import split_files
from mae.utils.func.util import remove_duplicates_globally


def create_pgvector(embedding, collection_name: str = 'doc', pg_connection: str = None)->PGVector:
    """
    Create a PGVector vector store instance.

    Parameters:
    embedding: Embedding model used to store vectors.
    collection_name (str, optional): Name of the collection to store vectors, default is 'doc'.
    pg_connection (str, optional): Connection string for the PostgreSQL database, default is 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain'.

    Returns:
    vectorstore: Created PGVector vector store instance.
    """

    if pg_connection is None:
        pg_connection = 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain'
    vectorstore = PGVector(
        embeddings=embedding,
        collection_name=collection_name,
        connection=pg_connection,
        use_jsonb=True,
    )
    return vectorstore



def delete_vector_collection(vectorstore:PGVector):
    """
    Delete the specified vector store collection.

    Parameters:
    vectorstore: PGVector vector store instance from which the collection is to be deleted.

    Returns:
    None.
    """

    vectorstore.drop_tables()

def upload_files_to_vector(vectorstore:PGVector, files_path: Union[List[str],str], chunk_size: int = 256, encoding: str = 'utf-8'):
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
    if len(docs) >=1:
        vectorstore.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
    else:
        print(f'{json.dumps(files_path)} Split File Is Empty')
    print('Data To Db  : ', time.time() - t1)

def search_vector(vectorstore:PGVector, keywords: Union[List[str],str], k: int = 4):
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
        results = vectorstore.similarity_search(keywords, k=k)

        for result in results:
            data.append(result.page_content)
        data = {keywords: list(set(data))}
    elif isinstance(keywords, list):
        data = []
        for keyword in keywords:
            results = vectorstore.similarity_search(keyword, k=k)
            data_values =  [item for d in data for sublist in d.values() for item in sublist]
            results = [item for item in results if item not in data_values]
            data.append({keyword: list(set([i.page_content for i in results]))})

    return remove_duplicates_globally(data)