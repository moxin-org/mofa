from langchain_postgres import PGVector


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

