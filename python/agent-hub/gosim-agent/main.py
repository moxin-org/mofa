import os

from mofa.kernel.rag.embedding.huggingface import load_embedding_model
from mofa.kernel.rag.vector.util import upload_files_to_vector, search_vector
from mofa.utils.database.vector.chromadb import create_chroma_db_conn_with_langchain
import json
import pathlib
from langchain.docstore.document import Document
from mofa.utils.files.split import create_documents_by_json_file
from mofa.utils.files.util import get_all_files
import uuid

# 生成一个 UUID 对象 (版本 4)


def create_generic_documents(data_list: list[dict]) -> list[Document]:
    """
    Converts a list of dictionaries into a list of LangChain Document objects generically.

    Each dictionary in the input list becomes one Document.
    - page_content: A string combining all key-value pairs from the dictionary.
    - metadata: Contains key-value pairs where the value is a simple type (str, int, float, bool).
    """
    documents = []
    if not isinstance(data_list, list):
        print("Error: Input data must be a list of dictionaries.")
        return documents

    for item in data_list:
        if not isinstance(item, dict):
            print(f"Warning: Skipping item because it is not a dictionary: {item}")
            continue

        content_parts = []
        metadata = {}

        for key, value in item.items():
            key_str = str(key) # Ensure key is a string

            # 1. Build page_content part (include all key-value pairs as strings)
            value_str = ""
            if isinstance(value, (str, int, float, bool)):
                value_str = str(value)
            elif isinstance(value, list) or isinstance(value, dict):
                # Convert lists/dicts to JSON string representation for content
                try:
                    value_str = json.dumps(value, ensure_ascii=False)
                except Exception:
                    value_str = str(value) # Fallback to basic string conversion
            elif value is None:
                value_str = "None"
            else:
                # Handle other potential types as strings
                value_str = str(value)

            content_parts.append(f"{key_str}: {value_str}")

            # 2. Build metadata (only include simple types)
            if isinstance(value, (str, int, float, bool)):
                 # Optional: Basic cleanup for metadata keys if needed
                 # metadata_key = key_str.replace('.', '_').replace(' ', '_') # Example cleanup
                 metadata[key_str] = value
            elif value is None:
                 metadata[key_str] = None # Store None directly if supported, or skip/stringify

        # Combine content parts into a single string for page_content
        page_content = "\n".join(content_parts)

        # Create the Document object
        if page_content: # Only create if there's some content
            doc = Document(id=uuid.uuid4().hex,page_content=page_content, metadata=metadata)
            documents.append(doc)
        else:
             print(f"Warning: Skipping empty dictionary or dictionary yielding no content: {item}")


    if not documents:
        print("Warning: No documents were created from the input list.")

    return documents
def gosim_json_vector(file_dir:str):
    files = get_all_files(file_dir, file_type="json")
    all_docs = []
    for file_path in files:
        if 'json' in pathlib.Path(file_path).suffix:
            with open(file_path, 'r', encoding='utf-8') as f:
                data_list = json.load(f)

        if isinstance(data_list, dict):
            for key in data_list.keys():
                if isinstance(data_list[key], list):
                    all_docs += create_generic_documents(data_list[key])
        elif isinstance(data_list, list):
            all_docs+= create_generic_documents(data_list)

    return all_docs
os.environ["OPENAI_API_KEY"] = '***REMOVED***'
model_name='text-embedding-3-large'
chroma_path = 'chroma_store'
json_path = '/Users/chenzi/chenzi/project/github/paris-2025/src/json'
md_path = '/Users/chenzi/chenzi/project/github/paris-2025/src/markdown'
embedding = load_embedding_model(model_name=model_name)
vectorstore = create_chroma_db_conn_with_langchain(embedding=embedding,db_path=chroma_path)
json_docs = gosim_json_vector(file_dir=json_path)

upload_files_to_vector(vectorstore=vectorstore, files_path=[json_path], chunk_size=256, encoding='utf-8', docs=json_docs)
md_files = get_all_files(md_path, file_type="md")
upload_files_to_vector(vectorstore=vectorstore,files_path=list(md_files), chunk_size=256, encoding='utf-8')


results = search_vector(vectorstore=vectorstore,keywords=['Paris'],k=6)
print(results)