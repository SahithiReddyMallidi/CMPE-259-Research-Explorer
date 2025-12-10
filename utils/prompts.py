def build_prompt(query, documents, strategy="basic"):
    context = "\n\n".join([f"Title: {d['title']}\nSummary: {d['summary']}" for d in documents])

    if strategy == "basic":
        return f"You are a research assistant. Use ONLY the context below to answer.\n\nContext:\n{context}\n\nQuestion: {query}\nAnswer:"

    elif strategy == "chaining":
        return f"Step 1: Extract key points from the context.\nStep 2: Summarize in simple language.\n\nContext:\n{context}\nQuestion: {query}\nAnswer:"

    elif strategy == "meta":
        return f"Act as an expert research assistant. Provide clear, concise answers with references to the context.\n\nContext:\n{context}\nQuestion: {query}\nAnswer:"

    elif strategy == "self_reflection":
        return f"Answer the question based on context, then review your answer for correctness and completeness.\n\nContext:\n{context}\nQuestion: {query}\nAnswer:"

    else:
        return f"Context:\n{context}\nQuestion: {query}\nAnswer:"
