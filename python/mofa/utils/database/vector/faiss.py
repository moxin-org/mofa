import json
import os
from typing import List

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
from attr import attrib, attrs, define, field

from mofa.utils.files.dir import make_dir
from mofa.utils.model.load import load_embedding_model_by_sentence_transformer

import pandas as pd

@define
class FaissIndex:
    faiss_dir_path = field(default='./faiss', type=str)
    model_path = field(default='./model/jinaai/jina-                           -v2-base-zh', type=str)
    dim = field(default=768, type=int)
    similarity_threshold = field(default=0.7, type=int)
    index = field(default=None)
    metadata = field(factory=list,type=list)
    model = field(default=None)
    faiss_index_file_name = field(default='faiss_index.bin', type=str)
    faiss_metadata_file_name = field(default='metadata.pkl', type=str)

    def __attrs_post_init__(self):
        self.model = load_embedding_model_by_sentence_transformer(model_path=self.model_path, trust_remote_code=True)
        self.index = faiss.IndexFlatL2(self.dim)
        make_dir(self.faiss_dir_path)


    @property
    def faiss_index_path(self):
        return os.path.join(self.faiss_dir_path, self.faiss_index_file_name)


    @property
    def faiss_metadata_path(self):
        return os.path.join(self.faiss_dir_path, self.faiss_metadata_file_name)


    def encode(self, texts:List[str]):
        return self.model.encode(texts)

    def add(self, documents:list[str]):
        # texts = [doc['page_content'] for doc in documents]
        vectors = self.encode(texts=documents)
        self.index.add(vectors)
        # for vector, doc in zip(vectors, documents):
        #     self.metadata.append({'page_content': doc['page_content'], 'metadata': doc['metadata']})


    def search(self, query_text, metadata_filter=None, similarity_threshold=None, k=10):
        if similarity_threshold is None:
            similarity_threshold = self.similarity_threshold
        query_vector = self.encode([query_text])[0]
        distances, indices = self.index.search(np.array([query_vector]), k)
        results = []
        for i, idx in enumerate(indices[0]):
            doc_data = self.metadata[idx]
            sim = 1 - distances[0][i] / (2 * self.dim)
            if sim >= similarity_threshold and self.metadata_matches(doc_data['metadata'], metadata_filter):
                results.append(
                    {'page_content': doc_data['page_content'], 'metadata': doc_data['metadata'], 'similarity': sim})
        return results

    def metadata_matches(self, doc_metadata, filter_criteria):
        if not filter_criteria:
            return True
        return all(doc_metadata.get(key) == value for key, value in filter_criteria.items())

    def save_index(self):
        """
        保存索引和元数据到指定目录。不删除原有目录和文件，仅更新文件。
        :param self.faiss_dir_path: 保存的目录路径。
        """

        # 保存FAISS索引
        faiss.write_index(self.index, self.faiss_index_path)

        # 保存元数据
        with open(self.faiss_metadata_file_name, 'wb') as f:
            pickle.dump(self.faiss_metadata_file_name, f)

    def load_index(self):


        # 加载FAISS索引
        self.index = faiss.read_index(self.faiss_index_path)

        # 加载元数据
        with open(self.faiss_metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)


