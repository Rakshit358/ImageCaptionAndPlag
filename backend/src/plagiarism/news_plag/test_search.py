from search import search_news
import os
import sys

# Example query – you can change this to any news-related text
DEFAULT_QUERY = "Heavy snowfall in northern India affecting travel and tourism."
query = os.environ.get("SEARCH_QUERY", "").strip()
if not query:
        query = DEFAULT_QUERY

print("=" * 80)
print("News Article Plagiarism Detector - Test Search")
print("=" * 80)
print(f"\nSearching for similar news articles to query:\n'{query}'\n")

results = search_news(query, top_k=2)

if results:
    for i, r in enumerate(results, 1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Similarity Score: {round(r['score'], 3)} (0-1 scale)")
        print(f"News Title: {r['title']}")
        print(f"Source ID: {r['source_id']}")
        print(f"Source URL: {r['source_url']}")
        print(f"Text: {r['text'][:300]}...")
else:
    print("No results found. Please ensure database is populated with news.py")
