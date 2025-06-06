import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_DB_PATH = "vector_store/faiss_index.bin"
METADATA_PATH = "vector_store/metadata.npy"


class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dim = 384  # embedding size for all-MiniLM-L6-v2
        self.index = None
        self.metadata = []
        self.load()

    def load(self):
        if os.path.exists(VECTOR_DB_PATH) and os.path.exists(METADATA_PATH):
            self.index = faiss.read_index(VECTOR_DB_PATH)
            self.metadata = list(np.load(METADATA_PATH, allow_pickle=True))
        else:
            self.index = faiss.IndexFlatIP(self.dim)  # inner product for cosine similarity
            self.metadata = []

    def save(self):
        if not os.path.exists("vector_store"):
            os.makedirs("vector_store")
        faiss.write_index(self.index, VECTOR_DB_PATH)
        np.save(METADATA_PATH, np.array(self.metadata, dtype=object))

    def embed(self, text):
        embedding = self.model.encode([text], convert_to_numpy=True)
        # Normalize embedding to unit length for cosine similarity with IP
        faiss.normalize_L2(embedding)
        return embedding[0]

    def add(self, input_text, output_text, source_path, domain_or_prompt, tags=None):
        tags = tags or []
        embedding = self.embed(input_text)
        self.index.add(np.array([embedding]))
        self.metadata.append({
            'input': input_text,
            'output': output_text,
            'source_path': source_path,
            'domain_or_prompt': domain_or_prompt,
            'tags': tags
        })
        self.save()

    def search(self, query_text, top_k=5):
        if self.index.ntotal == 0:
            return []
        query_emb = self.embed(query_text)
        D, I = self.index.search(np.array([query_emb]), top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.metadata):
                results.append({
                    'score': float(dist),
                    'metadata': self.metadata[idx]
                })
        return results

    def is_duplicate(self, input_text, threshold=0.92):
        if self.index.ntotal == 0:
            return False
        results = self.search(input_text, top_k=1)
        if results and results[0]['score'] >= threshold:
            return True
        return False

    def get_all_metadata(self):
        return self.metadata

    def get_tags(self):
        tags_set = set()
        for item in self.metadata:
            tags_set.update(item.get('tags', []))
        return sorted(list(tags_set))

    def search_by_tag(self, tag):
        return [m for m in self.metadata if tag in m.get('tags', [])]
