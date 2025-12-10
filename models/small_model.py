# models/small_model.py
from langchain_community.llms import Ollama
import time

class SmallModel:
    def __init__(self, model_name="mistral:7b"):
        # We use Ollama here because it uses 4-bit quantization automatically.
        print(f"[SmallModel] Connecting to {model_name} via Ollama...")
        self.llm = Ollama(model=model_name, temperature=0.2)
        print(f"[SmallModel] Connected successfully.")

    def generate(self, prompt, max_tokens=200):
        try:
            # We don't need manual tokenization here; Ollama handles it.
            return self.llm.invoke(prompt)
        except Exception as e:
            return f"Error generating answer: {e}"