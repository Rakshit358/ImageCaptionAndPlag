import sqlite3

conn = sqlite3.connect("paper_corpus.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM paper_chunks")
count = cur.fetchone()[0]

print("=" * 80)
print(f"Total chunks in paper_chunks: {count}")
print("=" * 80)

if count > 0:
    cur.execute("SELECT chunk_text, source_url, arxiv_id, paper_title FROM paper_chunks LIMIT 3")
    rows = cur.fetchall()

    for i, row in enumerate(rows, 1):
        print(f"\n--- Chunk {i} ---")
        print(f"Paper: {row[3]}")
        print(f"ArXiv ID: {row[2]}")
        print(f"Source: {row[1]}")
        print(f"Text: {row[0][:200]}...")
else:
    print("\nNo chunks found. Please run fetch_arxiv_papers.py first.")

conn.close()
