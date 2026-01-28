import numpy as np
import sqlite3
from sentence_transformers import SentenceTransformer, util
import torch

DB_PATH = "blog_corpus.db"
EMB_PATH = "embeddings.npy"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def load_embeddings():
    embeddings = np.load(EMB_PATH)
    return torch.tensor(embeddings)

def load_chunks_from_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT chunk_text,source_url FROM blog_chunks ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_blog(query_text,top_k=3):
    query_emb = model.encode(query_text,convert_to_tensor=True)
    embeddings = load_embeddings()
    # Move embeddings to same device as query
    embeddings = embeddings.to(query_emb.device)
    scores = util.cos_sim(query_emb,embeddings)[0]
    top_results = torch.topk(scores,k=top_k)
    rows = load_chunks_from_db()
    results = []
    for score, idx in zip(top_results.values, top_results.indices):
        chunk_text, source_url = rows[idx]
        results.append({
            "score": float(score),
            "text": chunk_text,
            "source": source_url
        })

    return results