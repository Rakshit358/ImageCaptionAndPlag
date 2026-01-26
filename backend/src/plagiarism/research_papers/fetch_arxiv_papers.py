import feedparser
import requests
from sentence_transformers import SentenceTransformer
from storage import init_db, insert_chunk, save_embeddings
import numpy as np
import time

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

init_db()

# ArXiv API endpoint
ARXIV_API = "http://export.arxiv.org/api/query?"

HEADERS = {
    "User-Agent": "AcademicResearchBot/1.0"
}

def fetch_arxiv_papers(search_query="machine learning", max_results=5):
    """
    Fetch papers from ArXiv API
    search_query: e.g., "machine learning", "deep learning", "neural networks"
    max_results: number of papers to fetch
    """
    params = {
        "search_query": f"cat:cs.LG AND {search_query}",  # Computer Science - Machine Learning category
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(ARXIV_API, params=params, headers=HEADERS, timeout=10)
    feed = feedparser.parse(response.content)
    
    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "summary": entry.summary,
            "arxiv_id": entry.id.split('/abs/')[-1],
            "authors": [author.name for author in entry.authors],
            "published": entry.published,
            "url": entry.id
        })
    
    return papers


def remove_newlines(text):
    """Clean up text by removing extra newlines and whitespace"""
    return " ".join(text.split())


def chunk_text(text, max_words=100):
    """Split text into chunks of approximately max_words"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        if len(chunk) > 100:  # Only keep chunks with meaningful content
            chunks.append(chunk)
    
    return chunks


def main():
    print("=" * 80)
    print("ArXiv Research Paper Plagiarism Detector - Data Fetching")
    print("=" * 80)
    
    # Fetch papers from ArXiv
    search_query = "machine learning"
    max_papers = 5
    
    print(f"\nFetching {max_papers} papers about '{search_query}' from ArXiv...")
    papers = fetch_arxiv_papers(search_query=search_query, max_results=max_papers)
    
    all_chunks = []
    all_embeddings = []
    
    for idx, paper in enumerate(papers, 1):
        print(f"\n[{idx}] TITLE: {paper['title']}")
        print(f"ArXiv ID: {paper['arxiv_id']}")
        print(f"URL: {paper['url']}")
        print(f"Authors: {', '.join(paper['authors'][:3])}")
        
        # Process abstract
        abstract = remove_newlines(paper['summary'])
        chunks = chunk_text(abstract)
        
        print(f"Generated {len(chunks)} chunks from abstract")
        
        # Generate embeddings and store
        for chunk_idx, chunk in enumerate(chunks):
            try:
                emb = model.encode(chunk)
                all_chunks.append(chunk)
                all_embeddings.append(emb)
                insert_chunk(chunk, paper['url'], paper['arxiv_id'], paper['title'])
                
                # Be polite to ArXiv servers
                time.sleep(0.1)
            except Exception as e:
                print(f"Error processing chunk {chunk_idx}: {e}")
                continue
        
        # Be polite to ArXiv API
        if idx < len(papers):
            time.sleep(2)
    
    # Save all embeddings
    if all_embeddings:
        embeddings_array = np.array(all_embeddings)
        save_embeddings(embeddings_array)
        print(f"\n{'=' * 80}")
        print(f"✓ Successfully stored {len(all_chunks)} chunks with embeddings")
        print(f"✓ Database saved as 'paper_corpus.db'")
        print(f"✓ Embeddings saved as 'embeddings.npy'")
        print(f"{'=' * 80}")
    else:
        print("No chunks were generated!")


if __name__ == "__main__":
    main()
