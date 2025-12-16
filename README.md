# CMPE-259 Research Explorer

## 📖 Project Overview
**Research Explorer** is an advanced Retrieval-Augmented Generation (RAG) system designed to query ArXiv research papers. Unlike standard RAG implementations, this project features a **Hybrid Search Architecture** (combining FAISS vector search with Tavily live web search), **Intelligent Model Routing** (switching between Small and Large LLMs), and robust **Security & Optimization** layers.

## 🚀 Key Features

* **Hybrid Retrieval:**
    * **Local:** Uses `FAISS` to search embedded ArXiv abstracts.
    * **Web:** Automatically triggers `Tavily` web search for queries about "trends", "news", or "recent" data (2024/2025).
* **Dual-Model Architecture:**
    * **Small Model:** Handles routing and simple tasks (Cost/Speed efficient).
    * **Large Model:** Handles complex reasoning and final answer generation.
* **Performance Optimization:**
    * Implemented `LRU Caching` to serve repeated queries instantly.
* **Security Guardrails:**
    * Input filtering to detect and block unsafe or malicious prompts before processing.
* **Automated Evaluation:**
    * Built-in scripts to test Intelligence (QA), Speed (Caching), and Safety.

```
## 📂 Project Structure

├── run.py                  # Main execution script (Runs Eval, Security & Speed tests)
├── rag/
│   ├── pipeline.py         # Core RAG logic (Safety -> Retrieve -> Generate)
│   ├── embedder.py         # Embedding generation
│   └── retriever.py        # Search logic (FAISS + Web)
├── models/
│   ├── small_model.py      # Wrapper for smaller LLM (e.g., Mistral/Llama-3-8b)
│   └── large_model.py      # Wrapper for larger LLM (e.g., Qwen/Llama-3-70b)
├── embeddings/             # FAISS vector store and build scripts
├── evaluation/             # Testing suites (Security, Caching, QA metrics)
└── data/                   # Raw ArXiv metadata (JSON)


## Installation and SetUp

1. Clone the repository

   git clone [https://github.com/SahithiReddyMallidi/CMPE-259-Research-Explorer.git](https://github.com/SahithiReddyMallidi/CMPE-259-Research-Explorer.git)
   cd CMPE-259-Research-Explorer

2. Install dependencies
   pip install -r requirements.txt

3. Environment Configuration Create a .env file in the root directory
   TAVILY_API_KEY=your_tavily_key_here

4. Setup Ollama (Local Models)
   ollama pull mistral
   ollama pull qwen:14b

## Usage
Running the Evaluation Pipeline
    python run.py

  This will:

  Build/Load the FAISS index.
  
  Run 20 Q&A test cases.
  
  Test the Caching mechanism (Speed).
  
  Test the Safety filters.

```
