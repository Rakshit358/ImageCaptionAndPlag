import sqlite3
import numpy as np
import os

DB_PATH = "blog_corpus.db"
EMB_PATH = "embeddings.npy"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS blog_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_text TEXT,
        source_url TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_chunk(chunk_text, source_url):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO blog_chunks (chunk_text, source_url) VALUES (?, ?)",
        (chunk_text, source_url)
    )

    conn.commit()
    conn.close()


def load_chunks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, chunk_text, source_url FROM blog_chunks")
    rows = cur.fetchall()

    conn.close()
    return rows


def save_embeddings(embeddings):
    np.save(EMB_PATH, embeddings)


def load_embeddings():
    if not os.path.exists(EMB_PATH):
        return None
    return np.load(EMB_PATH)
