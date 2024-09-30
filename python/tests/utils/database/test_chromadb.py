from mofa.utils.database.vector.chromadb import create_chroma_db_conn, add, query, delete, update
import pytest



def test_create_chroma_db_conn(mocker):
    mock_persistent_client = mocker.patch('utils.database.vector.chromadb.chromadb.PersistentClient')
    mock_client = mocker.patch('utils.database.vector.chromadb.chromadb.Client')

    mock_persistent_client.return_value.create_collection.return_value = "mock_conn"
    conn = create_chroma_db_conn(db_path='mock_path', collection_name='test_collection')
    mock_persistent_client.assert_called_once_with(path='mock_path')
    assert conn == "mock_conn"

    mock_client.return_value.create_collection.return_value = "mock_conn"
    conn = create_chroma_db_conn(db_path=None, collection_name='test_collection')
    mock_client.assert_called_once()
    assert conn == "mock_conn"


def test_add(mocker):
    mock_conn = mocker.MagicMock()

    documents = ["doc1", "doc2"]
    ids = [1, 2]
    add(mock_conn, documents, ids)
    mock_conn.add.assert_called_once_with(ids=['1', '2'], documents=documents)

    documents = ["doc1"]
    ids = [1, 2]
    with pytest.raises(ValueError, match="Length of documents and ids must be equal."):
        add(mock_conn, documents, ids)


def test_query(mocker):
    mock_conn = mocker.MagicMock()

    query_texts = ["search1", "search2"]
    mock_conn.query.return_value = {"results": "mock_results"}

    result = query(mock_conn, query_texts=query_texts, num_results=3)
    mock_conn.query.assert_called_once_with(query_texts=query_texts, n_results=3)
    assert result == {"results": "mock_results"}


def test_delete(mocker):
    mock_conn = mocker.MagicMock()

    ids = [1, 2]
    delete(mock_conn, ids)
    mock_conn.delete.assert_called_once_with(ids=['1', '2'])


def test_update(mocker):
    mock_conn = mocker.MagicMock()

    documents = ["doc1", "doc2"]
    ids = [1, 2]
    update(mock_conn, documents, ids)
    mock_conn.upsert.assert_called_once_with(ids=['1', '2'], documents=documents)
