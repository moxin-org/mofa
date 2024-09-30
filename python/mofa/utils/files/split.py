from langchain_text_splitters import RecursiveCharacterTextSplitter

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

