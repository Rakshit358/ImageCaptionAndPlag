import sqlite3

conn = sqlite3.connect("blog_corpus.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM blog_chunks")
count = cur.fetchone()[0]

print("Total rows in blog_chunks:", count)

cur.execute("SELECT chunk_text, source_url FROM blog_chunks LIMIT 3")
rows = cur.fetchall()

for i, row in enumerate(rows, 1):
    print(f"\n--- Row {i} ---")
    print("Source:", row[1])
    print("Text:", row[0][:200])

conn.close()
