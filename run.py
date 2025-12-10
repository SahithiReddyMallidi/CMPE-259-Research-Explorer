import os
from embeddings.build_faiss import build_index

from models.small_model import SmallModel
from models.large_model import LargeModel
from rag.pipeline import RAGPipeline

from evaluation.evaluate_system import run_evaluation, run_security_test, run_caching_test

JSON_PATH = "data/arxiv_metadata.json"
FAISS_PATH = "embeddings/vector_store.faiss"

def main():
    print("Step 1: Checking Vector Store (FAISS)...")
    if os.path.exists(FAISS_PATH) and os.path.exists("embeddings/meta.pkl"):
        print("FAISS index and metadata found. Skipping build.")
    else:
        print("FAISS index not found. Building now...")
        build_index(JSON_PATH, FAISS_PATH)

    print("\nStep 2: Initializing Models & RAG Pipeline...")
    # This connects to Ollama (Mistral + Qwen)
    small_model = SmallModel()
    large_model = LargeModel()
    rag = RAGPipeline(small_model=small_model, large_model=large_model)
    print("Pipeline ready.")

    print("\nStep 3: Running Project Evaluations...")
    
    # A. The Main 20 Questions (Intelligence Test)
    run_evaluation(rag) 
    
    # B. The Speed Test (Optimization Requirement)
    run_caching_test(rag)
    
    # C. The Safety Test (Security Requirement)
    run_security_test(rag)

    print("\nAll processes complete.")

if __name__ == "__main__":
    main()