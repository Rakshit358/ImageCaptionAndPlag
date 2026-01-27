import sqlite3

conn = sqlite3.connect("news_corpus.db")
cur = conn.cursor()

# Count total news chunks
cur.execute("SELECT COUNT(*) FROM news_chunks")
count = cur.fetchone()[0]

print("=" * 80)
print(f"Total chunks in news_chunks: {count}")
print("=" * 80)



if count > 0:
    # Fetch a few sample chunks
    cur.execute("""
        SELECT chunk_text, source_url,source_id, title
        FROM news_chunks
        LIMIT 3
    """)
    rows = cur.fetchall()

    for i, row in enumerate(rows, 1):
        print(f"\n--- News Chunk {i} ---")
        print(f"Title: {row[3]}")
        print(f"URL: {row[1]}")
        print(f"Id: {row[2]}")
        print(f"Text: {row[0][:200]}...")
else:
    print("\nNo news chunks found. Please run fetch_news.py first.")

conn.close()
