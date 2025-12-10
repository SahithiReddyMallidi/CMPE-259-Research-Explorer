import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from fastapi import FastAPI
from rag.pipeline import RAGPipeline
from models.small_model import SmallModel

app = FastAPI()

small = SmallModel()
rag = RAGPipeline(small_model=small)

@app.get("/ask")
def ask(q: str):
    return {"response": rag.answer(q)}
