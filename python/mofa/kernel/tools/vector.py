from typing import List, Union
import time
from langchain_postgres import PGVector

from mofa.kernel.rag.embedding.huggingface import load_embedding_model
from mofa.kernel.rag.split.util import split_files



# from mofa.utils.rag.split.util import split_files


def create_vector_collection_with_tool(module_path:str=None,model_name:str=None,multi_process:bool=False,model_kwargs:dict={'device':0}, collection_name: str = 'doc', pg_connection: str = None)->PGVector:
    """
    Create a PGVector vector store instance.

    Parameters:
    embedding: Embedding model used to store vectors.
    collection_name (str, optional): Name of the collection to store vectors, default is 'doc'.
    pg_connection (str, optional): Connection string for the PostgreSQL database, default is 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain'.

    Returns:
    vectorstore: Created PGVector vector store instance.
    """

    embedding = load_embedding_model(module_path=module_path,model_kwargs=model_kwargs,multi_process=multi_process,model_name=model_name)
    if pg_connection is None:
        pg_connection = 'postgresql+psycopg://langchain:langchain@localhost:6024/langchain'
    return PGVector(
        embeddings=embedding,
        collection_name=collection_name,
        connection=pg_connection,
        use_jsonb=True,
    )



def delete_vector_collection_with_tool(module_path:str=None,model_name:str=None,multi_process:bool=False,model_kwargs:dict={'device':0}, collection_name: str = 'doc', pg_connection: str = None):
    """
    Delete the specified vector store collection.

    Parameters:
    vectorstore: PGVector vector store instance from which to delete the collection.

    Returns:
    None.
    """

    vectorstore = create_vector_collection_with_tool(module_path=module_path,model_name=model_name,multi_process=multi_process,model_kwargs=model_kwargs, collection_name=collection_name, pg_connection = pg_connection)
    vectorstore.drop_tables()

def upload_files_to_vector_with_tool( files_path: List[str], chunk_size: int = 256, encoding: str = 'utf-8',module_path:str=None,model_name:str=None,multi_process:bool=False,model_kwargs:dict={'device':0}, collection_name: str = 'doc', pg_connection: str = None):
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
    vectorstore = create_vector_collection_with_tool(module_path=module_path,model_name=model_name,multi_process=multi_process,model_kwargs=model_kwargs, collection_name=collection_name, pg_connection = pg_connection)

    vectorstore.add_documents(docs, ids=[doc.metadata["id"] for doc in docs])
    print('当前数据入库完毕 : ', time.time() - t1)

def search_vector_with_tool( keywords: Union[List[str],str], k: int = 4,module_path:str=None,model_name:str=None,multi_process:bool=False,model_kwargs:dict={'device':0}, collection_name: str = 'doc', pg_connection: str = None):

    """
    Search for similar documents in the vector store.

    Parameters:
    vectorstore: PGVector vector store instance.
    keywords (str): Query string.
    k (int, optional): Number of similar documents to return, default is 4.

    Returns:
    similar_docs: List of similar documents.
    """

    vectorstore = create_vector_collection_with_tool(module_path=module_path,model_name=model_name,multi_process=multi_process,model_kwargs=model_kwargs, collection_name=collection_name, pg_connection = pg_connection)

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
            data.append({keyword: list(set([i.page_content for i in results]))})

    return data