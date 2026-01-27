from search import search_paper
import os
import sys

# Example query - you can change this to any research-related text
DEFAULT_QUERY = "Deep learning neural networks for image classification and pattern recognition."
query = os.environ.get("SEARCH_QUERY", "").strip()
if not query:
        query = DEFAULT_QUERY

print("=" * 80)
print("Research Paper Plagiarism Detector - Test Search")
print("=" * 80)
print(f"\nSearching for similar papers to query:\n'{query}'\n")

results = search_paper(query, top_k=3)

if results:
    for i, r in enumerate(results, 1):
        print("=" * 80)
        print(f"Result {i}")
        print(f"Similarity Score: {round(r['score'], 3)} (0-1 scale)")
        print(f"Paper Title: {r['paper_title']}")
        print(f"ArXiv ID: {r['arxiv_id']}")
        print(f"Source: {r['source']}")
        print(f"Text: {r['text'][:300]}...")
else:
    print("No results found. Please ensure database is populated with fetch_arxiv_papers.py")
