from langchain_community.llms import Ollama

class LargeModel:
    def __init__(self, model_name="qwen2.5:14b"):
        print(f"[LargeModel] Connecting to {model_name}...")
        self.llm = Ollama(model=model_name)

    def generate(self, prompt, max_tokens=250):
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            return f"Error: {e}"