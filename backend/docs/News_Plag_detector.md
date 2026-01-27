# News Articles Plagiarism Detector - Setup & Execution Guide

## Architecture Flow

```
User Query / News Text
↓
Light Preprocessing (Remove newlines, clean text)
↓
Semantic Embedding (SentenceTransformer)
↓
Vector Search (Cosine Similarity)
↓
Top-K candidate news chunks
↓
Similarity scoring with News metadata
↓
Plagiarism detection + source URLs
```

## Prerequisites & Installation

### Step 1: Install Required Dependencies

```bash
pip install requests sentence-transformers numpy torch sqlite3
```

> No API key is required for the Knowivate News API (free tier).

### Step 2: Navigate to Project Directory

```bash
cd src/plagiarism/news_articles
```

## Running the News Articles Detector

### Step 1: Fetch News Articles & Generate Embeddings

Run this first to populate the news corpus:

```bash
python fetch_news.py
```

**What this does:**

* Connects to Knowivate News API (free, public endpoint)
* Fetches latest news articles based on a query
* Extracts article metadata (title, URL, published date, description)
* Cleans and preprocesses article descriptions
* Splits content into ~100-word chunks
* Generates semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2`
* Stores chunks and metadata in SQLite database (`news_corpus.db`)
* Saves embeddings as a NumPy array (`embeddings.npy`)

**Customization Options:**

Modify parameters in `fetch_news.py`:

```python
query = "climate"     # Any topic (e.g., politics, AI, finance)
max_articles = 5        # Number of news articles to fetch
```

---

### Step 2: Verify Database Contents (Optional)

Check if news chunks were stored correctly:

```bash
python check_db.py
```

**What this does:**

* Displays total number of news chunks in the database
* Prints sample chunk text with article titles and URLs
* Confirms successful ingestion of news data

---

### Step 3: Test Plagiarism Detection

Run semantic similarity search on stored news articles:

```bash
python test_search.py
```

**What this does:**

* Takes a predefined query text (news paragraph or article)
* Encodes the query into an embedding
* Searches stored embeddings using cosine similarity
* Returns top-K most similar news chunks
* Displays similarity scores, article titles, and source URLs

**Customization:**

Modify the query in `test_search.py`:

```python
query = "Global warming policies are affecting coastal cities"
```

---

## Project Files Overview

| File                     | Purpose                                                                  |
| ------------------------ | ------------------------------------------------------------------------ |
| `fetch_news.py` | **Entry point** – Fetches news, generates embeddings, populates database |
| `storage.py`             | SQLite DB utilities (init DB, insert chunks, save/load embeddings)       |
| `search.py`              | Semantic search logic using cosine similarity                            |
| `check_db.py`            | Utility to inspect stored news chunks                                    |
| `test_search.py`         | Test script for plagiarism detection                                     |
| `embeddings.npy`         | Stored embeddings (auto-generated)                                       |
| `news_corpus.db`         | SQLite database storing news article chunks                              |

---

## Database Schema

### Table: `news_chunks`

| Column     | Type    | Description                     |
| ---------- | ------- | ------------------------------- |
| id         | INTEGER | Primary key, auto-increment     |
| chunk_text | TEXT    | Chunk of news article content   |
| source_url | TEXT    | Original news article URL       |
| source_id  | TEXT    | Unique news/article ID from API |
| title      | TEXT    | News article title              |

---

## Key Components

### Data Source: Knowivate News API

* **Endpoint:** `https://news.knowivate.com/api/news`
* **Coverage:** Latest national & international news
* **Authentication:** None required (free tier)
* **Filtering:** Supports query-based search (`q` parameter)

---

### Embedding Model

* **Model:** `sentence-transformers/all-MiniLM-L6-v2`
* **Embedding Size:** 384 dimensions
* **Purpose:** Converts news text into semantic vectors
* **Benefit:** Detects semantic plagiarism beyond exact wording

---

### Search Method

* **Algorithm:** Cosine Similarity

* **Process:**

  1. Encode query text into embedding
  2. Compare query vector against stored embeddings
  3. Compute cosine similarity scores
  4. Return top-K similar news chunks

* **Score Range:**

  * `1.0` → Identical meaning
  * `0.7+` → High semantic similarity
  * `<0.4` → Weak or unrelated content

---

## Troubleshooting

### API Returns Very Few Articles

* The free endpoint may return limited results
* Try different queries or broader keywords
* Increase `max_articles` gradually

---

### Missing Database or Embeddings

* Ensure `fetch_news.py` ran successfully
* Check that `news_corpus.db` and `embeddings.npy` exist

---

### No Similar Results Found

* Verify database contains data using `check_db.py`
* Ensure query topic matches stored news
* Increase `top_k` value in `test_search.py`

---

## Performance Notes

* **First Run:** 10–30 seconds (depends on number of articles)
* **Search Time:** <1 second for hundreds of chunks
* **Embedding Generation:** ~0.05–0.1 seconds per chunk
* **Database Size:** Small (<5MB for hundreds of chunks)

---

## Advanced Usage

### Multiple Topics Ingestion

```python
topics = ["climate", "artificial intelligence", "elections"]

for topic in topics:
    fetch_news_articles(query=topic, max_articles=3)
```

---

### Adjusting Similarity Threshold

```python
min_score = 0.75
results = [r for r in results if r['score'] >= min_score]
```

---

### Using Higher-Quality Embeddings

```python
# Better semantic quality (slower)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Scientific/news focused
model = SentenceTransformer("sentence-transformers/allenai-specter")
```

---

## Comparison: Research Papers vs News Detector

| Aspect           | Research Papers Detector | News Articles Detector |
| ---------------- | ------------------------ | ---------------------- |
| Data Source      | ArXiv API                | Knowivate News API     |
| Text Type        | Abstracts                | News descriptions      |
| Chunk Size       | 100 words                | 80–100 words           |
| Metadata         | ArXiv ID, Title          | Article ID, URL        |
| Update Frequency | Static                   | Real-time              |
| API Key Required | No                       | No                     |

---

## Related Documentation

* Research paper plagiarism setup: `Research_Paper_Plag_Detector.md`
* Blog plagiarism detector: `Blog_Plag_detector.md`
* Image captioning setup: `INSTALLATION.md`
