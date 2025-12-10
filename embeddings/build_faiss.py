from sentence_transformers import SentenceTransformer
import faiss
import json
import pickle
from tqdm import tqdm
import numpy as np
import os

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 5000  # smaller chunks for faster and stable embedding

def load_metadata(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except:
                continue
    return data

def build_index(json_path, index_path="embeddings/vector_store.faiss"):
    print("Loading metadata...")
    papers = load_metadata(json_path)
    
    embedder = SentenceTransformer(MODEL_NAME, device="cpu")
    print(f"Using device: {embedder.device}")
    
    # Prepare texts
    texts = [(p.get("title", "") or "") + " " + (p.get("summary", "") or "") for p in papers]
    
    print("Embedding papers in chunks...")
    all_embeddings = []

    for i in tqdm(range(0, len(texts), CHUNK_SIZE), desc="Encoding chunks"):
        batch = texts[i:i+CHUNK_SIZE]
        emb = embedder.encode(batch, convert_to_numpy=True, normalize_embeddings=True).astype("float32")
        all_embeddings.append(emb)
        
        # Optional: save chunk to disk to avoid losing progress
        os.makedirs("embeddings/chunks", exist_ok=True)
        np.save(f"embeddings/chunks/chunk_{i//CHUNK_SIZE}.npy", emb)

    # Concatenate all embeddings
    embeddings = np.vstack(all_embeddings)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    # Save metadata
    with open("embeddings/meta.pkl", "wb") as f:
        pickle.dump(papers, f)

    print("FAISS index created successfully.")

if __name__ == "__main__":
    build_index("data/arxiv_metadata.json")
