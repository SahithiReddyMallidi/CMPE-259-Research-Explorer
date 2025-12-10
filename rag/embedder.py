from sentence_transformers import SentenceTransformer
import torch

DEVICE = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

class Embedder:
    def __init__(self, model="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model, device=DEVICE)

    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)
