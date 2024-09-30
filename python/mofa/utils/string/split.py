from langchain.text_splitter import CharacterTextSplitter
from mofa.utils.variable.util import generate_unique_int

def split_str_to_docs(string:str,chunk_size:int=328,):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=chunk_size,
        chunk_overlap=200,
    )
    docs = text_splitter.create_documents([string])
    all_docs = []
    for doc in docs:
        doc.metadata['id'] = generate_unique_int()
        all_docs.append(doc)
    return all_docs