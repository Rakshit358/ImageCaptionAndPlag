import sqlite3
import numpy as np
import os

DB_PATH = "news_corpus.db"
EMB_PATH = "embeddings.npy"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_chunks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chunk_text TEXT,
        source_url TEXT,
        source_id TEXT,
        title TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_chunk(chunk_text, source_url, source_id, title):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO news_chunks 
        (chunk_text, source_url, source_id, title)
        VALUES (?, ?, ?, ?)
        """,
        (chunk_text, source_url, source_id, title)
    )

    conn.commit()
    conn.close()


def load_chunks():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, chunk_text, source_url, source_id, title
        FROM news_chunks
    """)
    rows = cur.fetchall()

    conn.close()
    return rows


def save_embeddings(embeddings):
    np.save(EMB_PATH, embeddings)


def load_embeddings():
    if not os.path.exists(EMB_PATH):
        return None
    return np.load(EMB_PATH)
