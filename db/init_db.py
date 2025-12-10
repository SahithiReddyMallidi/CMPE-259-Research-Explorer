import sqlite3
import json
from tqdm import tqdm

def load_jsonl_or_json(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data.append(json.loads(line))
            except:
                continue
    return data

def init_db(json_path, db_path="db/arxiv.db"):
    print("Loading metadata (this may take time)...")
    papers = load_jsonl_or_json(json_path)
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id TEXT PRIMARY KEY,
        title TEXT,
        authors TEXT,
        summary TEXT,
        categories TEXT,
        published TEXT
    )
    """)

    for p in tqdm(papers):
        c.execute("""
        INSERT OR REPLACE INTO papers
        (id, title, authors, summary, categories, published)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            p.get("id"),
            p.get("title"),
            ", ".join(p.get("authors", [])),
            p.get("summary"),
            p.get("categories"),
            p.get("published"),
        ))

    conn.commit()
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    init_db("data/arxiv_metadata.json")
