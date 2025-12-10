import sqlite3

def query_db(db_path, keyword):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    q = f"SELECT title, summary FROM papers WHERE summary LIKE '%{keyword}%' LIMIT 5"
    res = c.execute(q).fetchall()
    conn.close()
    return res
