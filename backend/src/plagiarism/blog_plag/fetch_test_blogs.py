import feedparser
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer, util
from storage import init_db, insert_chunk, save_embeddings
import numpy as np


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

init_db()

DEVTO_FEED = "https://dev.to/feed"

HEADERS = {
    "User-Agent": "AcademicResearchBot/1.0"
}

def fetch_blog_urls(limit=5):
    feed = feedparser.parse(DEVTO_FEED)
    urls = []

    for entry in feed.entries[:limit]:
        urls.append({
            "title": entry.title,
            "url": entry.link
        })

    return urls

def remove_boilerplate(text):
    blacklist_phrases = [
        "Originally published at",
        "Posted on",
        "Subscribe to get",
        "Templates let you",
        "Are you sure you want to hide",
        "For further actions",
        "reporting abuse"
    ]

    lines = text.split("\n")
    clean_lines = []

    for line in lines:
        if not any(phrase.lower() in line.lower() for phrase in blacklist_phrases):
            clean_lines.append(line)

    return " ".join(clean_lines)


def extract_blog_text(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    article = soup.find("article")
    if not article:
        return ""

    paragraphs = []
    for p in article.find_all("p"):
        text = p.get_text().strip()
        if len(text) > 60: 
            paragraphs.append(text)

    return "\n".join(paragraphs)


def chunk_text(text, max_words=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        if len(chunk) > 100:
            chunks.append(chunk)

    return chunks

all_chunks = []
all_embeddings = []

def main():
    blogs = fetch_blog_urls(limit=1)

    for idx, blog in enumerate(blogs, 1):
        print(f"[{idx}] TITLE: {blog['title']}")
        print(f"SOURCE: {blog['url']}\n")
        text = extract_blog_text(blog["url"])
        filter_text = remove_boilerplate(text)
        chunks = chunk_text(filter_text)
    
    print(chunks)

    for chunk in chunks:
        emb = model.encode(chunk)
        all_chunks.append(chunk)
        all_embeddings.append(emb)
        insert_chunk(chunk,blog["url"])

    save_embeddings(np.array(all_embeddings))

if __name__ == "__main__":
    main()
