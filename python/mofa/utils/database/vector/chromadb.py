import os
from typing import Union
import chromadb
from langchain_chroma import Chroma


def create_chroma_db_conn(db_path: Union[str, None] = '.', collection_name: str = 'mofa', *args, **kwargs):
    """
    Create or connect to a Chroma database collection and return the collection.

    :param db_path: Database path, defaults to current directory ('.').
    :param collection_name: Collection name, defaults to 'default'.
    :param args: Other positional arguments.
    :param kwargs: Other keyword arguments.
    :return: Chroma collection connection.
    """
    try:
        # 创建ChromaDB客户端
        if db_path is not None:
            client = chromadb.PersistentClient(path=db_path)
        else:
            client = chromadb.Client()

        # 检查集合是否存在
        conn = client.get_or_create_collection(name=collection_name,**kwargs)
        return conn
    except Exception as e:
        raise RuntimeError(f"Error creating or connecting to Chroma DB collection: {e}")
def add(conn, documents: list, ids: list,metadatas:Union[list,None]=None,batch_size: int = 5000, *args, **kwargs):
    """
    Add documents to the ChromaDB database with corresponding IDs.

    :param conn: ChromaDB connection instance.
    :param documents: List of documents to be added to the database.
    :param ids: List of IDs corresponding to the documents. Must be the same length as the documents list.
    :param args: Other positional arguments.
    :param kwargs: Other keyword arguments for the add operation.
    :raises ValueError: If the length of documents and ids is not equal.
    """
    if len(documents) != len(ids):
        raise ValueError("Length of documents and ids must be equal.")
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    if len(ids)<= batch_size and len(ids)<41555:
        conn.add(documents=documents, ids=ids, **kwargs)
    else:
        for i in range(0, len(documents), batch_size):
            batch_documents = documents[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            if metadatas is not None:
                batch_metadatas = metadatas[i:i + batch_size]
                conn.add(
                    documents=batch_documents,
                    metadatas=batch_metadatas,
                    ids=batch_ids,**kwargs
                )
            else:
                conn.add(
                    documents=batch_documents,
                    ids=batch_ids, **kwargs
                )


def query(conn, query_texts: list, num_results: int = 3, *args, **kwargs):
    """
    Query documents from the ChromaDB database based on the provided query texts.

    :param conn: ChromaDB connection instance.
    :param query_texts: List of query texts to search for in the database.
    :param num_results: Number of results to return per query, defaults to 3.
    :param args: Other positional arguments.
    :param kwargs: Other keyword arguments for the query operation.
    :return: Query results from the database.
    """
    query_texts = [str(text) if not isinstance(text, str) else text for text in query_texts]
    results = conn.query(
        query_texts=query_texts,  # Chroma will embed this for you
        n_results=num_results,
        **kwargs
    )
    return results


def delete(conn, ids: list, *args, **kwargs):
    """
    Delete documents from the ChromaDB database based on the provided IDs.

    :param conn: ChromaDB connection instance.
    :param ids: List of document IDs to be deleted.
    :param args: Other positional arguments.
    :param kwargs: Other keyword arguments for the delete operation.
    """
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    conn.delete(ids=ids, **kwargs)


def update(conn, documents: list, ids: list, *args, **kwargs):
    """
    Update or upsert documents in the ChromaDB database with corresponding IDs.

    :param conn: ChromaDB connection instance.
    :param documents: List of documents to update or insert into the database.
    :param ids: List of IDs corresponding to the documents.
    :param args: Other positional arguments.
    :param kwargs: Other keyword arguments for the upsert operation.
    """
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    conn.upsert(ids=ids, documents=documents, **kwargs)
def create_chroma_db_conn_with_langchain(embedding, db_path: Union[str, None] = '.', collection_name: str = 'mofa', *args, **kwargs):
    """
    Create a Chroma vector store connection with Langchain embedding.

    :param embedding: Embedding function to be used for the documents.
    :param db_path: Directory path where the Chroma database will be persisted, defaults to current directory ('.').
    :param collection_name: Name of the collection, defaults to 'mofa'.
    :param args: Additional positional arguments.
    :param kwargs: Additional keyword arguments for the vector store initialization.
    :return: Chroma vector store instance.

    For more methods and detailed information, please refer to the official documentation
    https://python.langchain.com/v0.2/docs/integrations/vectorstores/chroma/
    """
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_path,
        embedding_function=embedding,
        **kwargs
    )
    return vector_store


def add_with_langchain(vector_conn, documents: list, ids: list):
    """
    Add documents to the Chroma vector store with corresponding IDs.

    :param vector_conn: Chroma vector store connection instance.
    :param documents: List of documents to be added.
    :param ids: List of IDs corresponding to the documents. Must be the same length as the documents list.
    :raises ValueError: If the length of documents and ids is not equal.
    """
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    vector_conn.add_documents(documents=documents, ids=ids)


def update_with_langchain(vector_conn, documents: list, ids: list):
    """
    Update or upsert documents in the Chroma vector store with corresponding IDs.

    :param vector_conn: Chroma vector store connection instance.
    :param documents: List of documents to update or insert into the vector store.
    :param ids: List of IDs corresponding to the documents.
    :raises ValueError: If the length of documents and ids is not equal.
    """
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    vector_conn.update_documents(documents=documents, ids=ids)


def delete_with_langchain(vector_conn, ids: list):
    """
    Delete documents from the Chroma vector store based on the provided IDs.

    :param vector_conn: Chroma vector store connection instance.
    :param ids: List of document IDs to be deleted.
    """
    ids = [str(id) if not isinstance(id, str) else id for id in ids]
    vector_conn.delete(ids=ids)


def query_with_langchain(vector_conn, query_texts: str, embedding, num_results: int = 3, search_type: str = 'similarity_search', **kwargs) -> list[str]:
    """
    Query documents from the Chroma vector store using similarity search or similarity score.

    :param vector_conn: Chroma vector store connection instance.
    :param query_texts: Query string to search for in the vector store.
    :param embedding: Embedding function to embed the query text.
    :param num_results: Number of results to return, defaults to 3.
    :param search_type: Type of search to perform ('similarity_search', 'similarity_score', etc.), defaults to 'similarity_search'.
    :param kwargs: Additional keyword arguments for the search operation.
    :return: List of page contents from the query results.
    """
    result_data = []
    if search_type == 'similarity_search':
        results = vector_conn.similarity_search_by_vector(
            embedding=embedding.embed_query(query_texts), k=num_results, **kwargs
        )
    elif search_type == 'similarity_score':
        results = vector_conn.similarity_search_with_score(
            query_texts, k=num_results, **kwargs
        )
    else:
        results = vector_conn.similarity_search(
            query_texts, k=num_results, **kwargs
        )
    for doc in results:
        result_data.append(doc.page_content)
    return result_data
