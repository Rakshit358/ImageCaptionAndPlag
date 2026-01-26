import sqlite3
import numpy as np
import os

DB_PATH = "paper_corpus.db"
EMB_PATH = "embeddings.npy"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS paper_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_text TEXT,
        source_url TEXT,
        arxiv_id TEXT,
        paper_title TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_chunk(chunk_text, source_url, arxiv_id, paper_title):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO paper_chunks (chunk_text, source_url, arxiv_id, paper_title) VALUES (?, ?, ?, ?)",
        (chunk_text, source_url, arxiv_id, paper_title)
    )

    conn.commit()
    conn.close()


def load_chunks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, chunk_text, source_url, arxiv_id, paper_title FROM paper_chunks")
    rows = cur.fetchall()

    conn.close()
    return rows


def save_embeddings(embeddings):
    np.save(EMB_PATH, embeddings)


def load_embeddings():
    if not os.path.exists(EMB_PATH):
        return None
    return np.load(EMB_PATH)
