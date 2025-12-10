# rag/retriever.py
import os
import sqlite3
import pickle
import faiss
import numpy as np

class Retriever:
    def __init__(self, index_path="embeddings/vector_store.faiss", meta_path="embeddings/meta.pkl", db_path="db/arxiv.db"):
        # Load FAISS index
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}. Please build it first.")
        self.index = faiss.read_index(index_path)

        # Load metadata
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata not found at {meta_path}. Please build it first.")
        with open(meta_path, "rb") as f:
            self.metadata = pickle.load(f)

        self.db_path = db_path

    def search_faiss(self, query_emb, k=5):
        query_emb = np.array([query_emb], dtype="float32")
        if query_emb.shape[1] != self.index.d:
            raise ValueError(f"Embedding dimension mismatch! Query dim: {query_emb.shape[1]}, FAISS index dim: {self.index.d}")
        scores, idx = self.index.search(query_emb, k)

        docs = []
        for i in idx[0]:
            doc = self.metadata[i].copy()
            # Ensure 'summary' key exists for prompt building
            if 'summary' not in doc and 'abstract' in doc:
                doc['summary'] = doc['abstract']
            elif 'summary' not in doc:
                doc['summary'] = ""
            docs.append(doc)
        return docs


    def query_db(self, keyword, limit=5):
        if not os.path.exists(self.db_path):
            print(f"[Retriever] Database not found at {self.db_path}")
            return []
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        q = "SELECT title, summary FROM papers WHERE summary LIKE ? LIMIT ?"
        res = c.execute(q, (f"%{keyword}%", limit)).fetchall()
        conn.close()
        return [{"title": r[0], "summary": r[1]} for r in res]

    def search_all(self, query_emb, keyword=None, use_db=True):
        docs = self.search_faiss(query_emb)
        if use_db and keyword:
            docs += self.query_db(keyword)
        return docs[:10]  # limit to top 10
