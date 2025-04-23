import json
import pathlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

from mofa.utils.files.read import read_text


def split_txt_by_langchain(chuck_size: int = 1024, chuck_overlap: int = 0,
                           file_path: str = '/mnt/d/project/dy/extra/nlp/uie/三体1疯狂年代.txt',encoding:str='utf-8') -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chuck_size,
        chunk_overlap=chuck_overlap,
        length_function=len,
    )
    texts = text_splitter.split_text(read_text(file_path=file_path,encoding=encoding))
    return texts

def create_documents_by_json_file(file_path:str) -> list[Document]:
    """
    Converts a list of dictionaries into a list of LangChain Document objects generically.

    Each dictionary in the input list becomes one Document.
    - page_content: A string combining all key-value pairs from the dictionary.
    - metadata: Contains key-value pairs where the value is a simple type (str, int, float, bool).
    """
    if 'json' in pathlib.Path(file_path).suffix:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
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
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
        else:
             print(f"Warning: Skipping empty dictionary or dictionary yielding no content: {item}")


    if not documents:
        print("Warning: No documents were created from the input list.")

    return documents