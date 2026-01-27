from search import search_blog
import os
import sys

DEFAULT_QUERY = "Programming ecosystem of C exists but as isolated domains with inconsistent syntax."
query = os.environ.get("SEARCH_QUERY", "").strip()
if not query:
        query = DEFAULT_QUERY

results = search_blog(query, top_k=1)

for i, r in enumerate(results, 1):
    print("=" * 80)
    print(f"Result {i}")
    print("Score:", round(r["score"], 3))
    print("Source:", r["source"])
    print("Text:", r["text"][:300], "...")
