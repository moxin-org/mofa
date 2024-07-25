from sentence_transformers import SentenceTransformer
from numpy.linalg import norm
def load_embedding_model_by_sentence_transformer(model_path:str,trust_remote_code:bool=True):
    """
    Loads the embeddings from a file.

    Args:
        file_
    """

    model = SentenceTransformer( model_path, trust_remote_code=trust_remote_code)
    return model
