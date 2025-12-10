# rag/pipeline.py
from rag.embedder import Embedder
from rag.retriever import Retriever
from utils.prompts import build_prompt
from tools.web_search import web_search
from functools import lru_cache
from utils.safety import is_safe

class RAGPipeline:
    def __init__(self, small_model=None, large_model=None):
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.model_small = small_model
        self.model_large = large_model      

    @lru_cache(maxsize=1000) 
    def answer(self, query, strategy="basic", use_db=True, use_large=False): 
        # 1. Safety Check
        if not is_safe(query): 
            print(f"Security Block triggered for query: {query}")
            return "Query rejected due to unsafe/lengthy content."
        
        # 2. Vector Search (Tool 1: Database)
        query_emb = self.embedder.encode([query])[0] 
        keyword = query.split()[0] if use_db else None 
        
        # Get DB docs
        db_docs = self.retriever.search_all(query_emb, keyword, use_db) 

        # 3. Web Search (Tool 2: Web)
        # Logic: Search web if DB is empty OR if query asks for "new/recent/trends"
        web_docs = []
        needs_web = (not db_docs) or any(w in query.lower() for w in ["recent", "trend", "news", "2024", "2025", "latest"])
        
        if needs_web:
            print(f"Triggering Web Search for: {query}")
            try:
                web_results = web_search(query)
                # Convert Tavily format to match your DB format
                web_docs = [{"title": r['title'], "summary": r['content']} for r in web_results]
            except Exception as e:
                print(f"Web search failed: {e}")

        # 4. Merge Data (Combine both sources)
        # We put web docs first if the user asked for "recent", otherwise DB first
        if "recent" in query.lower() or "trend" in query.lower():
            combined_docs = web_docs + db_docs
        else:
            combined_docs = db_docs + web_docs

        # 5. Generate Answer
        # If we have absolutely no data from either source, warn the model
        if not combined_docs:
            return "I couldn't find any relevant information in the database or on the web."

        prompt = build_prompt(query, combined_docs, strategy) 
        model = self.model_large if use_large else self.model_small 
        return model.generate(prompt)