import requests
import time
import numpy as np
from sentence_transformers import SentenceTransformer
from storage import init_db, insert_chunk, save_embeddings



model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

init_db()
NEWS_API = "https://news.knowivate.com/api/news"
HEADERS = {
    "User-Agent": "AcademicResearchBot/1.0"
}

def fetch_news_articles(query: str, max_articles: int = 5):
    """
    Fetch news articles from Knowivate News API
    """
    params = {
        "q": query,
        "limit": max_articles
    }
    response = requests.get(NEWS_API, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()

    news = []

    for item in data.get("news", []):
        news.append({
            "id": item.get("_id"),
            "url": item.get("url"),
            "title": item.get("title"),
            "publishedAt": item.get("publishedAt"),
            "description": item.get("description")
        })
    return news


def remove_newlines(text: str) -> str:
    return " ".join(text.split())

def chunk_text(text: str, max_words: int = 100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        if len(chunk) > 100:
            chunks.append(chunk)

    return chunks

def main():
    print("=" * 80)
    print("News Article Plagiarism Detector - Data Fetching")
    print("=" * 80)

    query = "climate"
    max_articles=3
    print(f"\nFetching {max_articles} news articles about '{query}'...")
    all_News = fetch_news_articles(query=query, max_articles=max_articles)
    
    all_chunks=[]
    all_embeddings=[]

    for idx, article in enumerate(all_News, 1):
        print(f"\n[{idx}] TITLE: {article['title']}")
        print(f"Published At: {article['publishedAt']}")
        print(f"URL: {article['url']}")

        description = article.get("description") or ""
        content = remove_newlines(description)
        chunks = chunk_text(content)

        print(f"Generated {len(chunks)} chunks")

        for chunk_idx, chunk in enumerate(chunks):
            try:
                embedding = model.encode(chunk)

                all_chunks.append(chunk)
                all_embeddings.append(embedding)

                insert_chunk(
                    chunk_text=chunk,
                    source_url=article["url"],
                    source_id=article["id"],
                    title=article["title"]
                )
                time.sleep(0.1)

            except Exception as e:
                print(f"Error processing chunk {chunk_idx}: {e}")
            
    if all_embeddings:
        embeddings_array = np.array(all_embeddings)
        save_embeddings(embeddings_array)

        print(f"\n{'=' * 80}")
        print(f" Stored {len(all_chunks)} news chunks")
        print(f" Database saved successfully")
        print(f" Embeddings saved as embeddings.npy")
        print(f"{'=' * 80}")
    else:
        print("No chunks generated!")



if __name__ == "__main__":
    main()
