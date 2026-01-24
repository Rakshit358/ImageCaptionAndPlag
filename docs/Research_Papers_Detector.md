# Research Papers Plagiarism Detector - Setup & Execution Guide

## Architecture Flow

```
Research Query/Abstract
↓
Light Preprocessing (Remove newlines, clean text)
↓
Semantic Embedding (SentenceTransformer)
↓
Vector Search (Cosine Similarity)
↓
Top-K candidate paper chunks
↓
Similarity scoring with ArXiv metadata
↓
Plagiarism detection + sources
```

## Prerequisites & Installation

### Step 1: Install Required Dependencies

```bash
pip install feedparser requests beautifulsoup4 sentence-transformers numpy torch sqlite3
```

### Step 2: Navigate to Project Directory

```bash
cd src/plagiarism/research_papers
```

## Running the Research Papers Detector

### Step 1: Fetch ArXiv Papers & Generate Embeddings

Run this first to populate the research paper corpus with embeddings:

```bash
python fetch_arxiv_papers.py
```

**What this does:**

- Connects to ArXiv API (free, no authentication required)
- Fetches research papers from Computer Science - Machine Learning category
- Extracts paper metadata (title, authors, abstract, ArXiv ID)
- Cleans and preprocesses abstract text
- Splits abstracts into 100-word chunks
- Generates semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores chunks and metadata in SQLite database (`paper_corpus.db`)
- Saves embeddings as numpy array (`embeddings.npy`)
- Respects ArXiv API rate limits with polite 2-second delays between requests

**Customization Options:**

Modify the search parameters in `fetch_arxiv_papers.py`:

```python
search_query = "machine learning"  # Change to any research topic
max_papers = 5                      # Number of papers to fetch
```

### Step 2: Verify Database Contents (Optional)

Check if papers were successfully stored:

```bash
python check_db.py
```

**What this does:**

- Shows total number of paper chunks in database
- Displays sample entries with paper titles, ArXiv IDs, and abstracts
- Confirms embeddings were generated correctly

### Step 3: Test Plagiarism Detection

Run semantic similarity search on stored research papers:

```bash
python test_search.py
```

**What this does:**

- Takes a predefined query text (research abstract or question)
- Searches the paper corpus using cosine similarity
- Returns top-3 most similar paper chunks with similarity scores
- Shows paper titles, ArXiv IDs, and source URLs
- Displays the actual matching text from papers

**Customization:**

Modify the query in `test_search.py`:

```python
query = "Your research abstract or plagiarism check text here"
```

## Project Files Overview

| File                    | Purpose                                                                                 |
| ----------------------- | --------------------------------------------------------------------------------------- |
| `fetch_arxiv_papers.py` | **Entry point** - Fetches papers from ArXiv API, creates embeddings, populates database |
| `storage.py`            | Database operations (init, insert chunks with metadata, save/load embeddings)           |
| `search.py`             | Core search logic using semantic similarity (cosine distance)                           |
| `check_db.py`           | Utility to inspect database contents and verify paper storage                           |
| `test_search.py`        | Test script to query the plagiarism detector                                            |
| `embeddings.npy`        | Pre-computed embeddings file (auto-generated)                                           |
| `paper_corpus.db`       | SQLite database storing research paper chunks (auto-generated)                          |

## Complete Workflow Example

```bash
# 1. Fetch papers and populate corpus (takes 1-2 minutes)
python fetch_arxiv_papers.py

# 2. Verify papers were stored
python check_db.py

# 3. Test plagiarism detection with sample query
python test_search.py
```

## Database Schema

### Table: `paper_chunks`

| Column      | Type    | Description                                |
| ----------- | ------- | ------------------------------------------ |
| id          | INTEGER | Primary key, auto-increment                |
| chunk_text  | TEXT    | 100-word chunk of paper abstract           |
| source_url  | TEXT    | Full ArXiv URL to paper                    |
| arxiv_id    | TEXT    | Unique ArXiv identifier (e.g., 2301.12345) |
| paper_title | TEXT    | Full title of research paper               |

## Key Components

### Data Source: ArXiv API

- **Endpoint:** `http://export.arxiv.org/api/query?`
- **Coverage:** 2.4M+ papers in physics, math, CS, biology, finance, statistics
- **Authentication:** None required (free, public API)
- **Rate Limit:** 3+ seconds between requests (our code uses 2 seconds - polite crawling)

### Embedding Model

- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension:** 384-dimensional vectors
- **Purpose:** Converts text chunks into semantic embeddings
- **Why:** Enables semantic similarity search beyond keyword matching

### Search Method

- **Algorithm:** Cosine Similarity
- **Process:**
  1. Encodes query into embedding vector
  2. Compares query embedding against all stored embeddings
  3. Calculates cosine distance between vectors
  4. Returns top-K matches
- **Output:** Similarity scores from 0-1 (1 = identical, 0 = unrelated)

## ArXiv API Configuration

### Supported Categories (in `fetch_arxiv_papers.py`)

Currently configured for Computer Science - Machine Learning:

```python
search_query = "cat:cs.LG AND machine learning"
```

**To search other categories, modify the search_query:**

| Category              | Code       | Examples               |
| --------------------- | ---------- | ---------------------- |
| Computer Science - AI | cs.AI      | "cat:cs.AI"            |
| Computer Science - CV | cs.CV      | "cat:cs.CV"            |
| Mathematics           | math.\*    | "cat:math.AP"          |
| Physics               | physics.\* | "cat:physics.quant-ph" |

**Example: To search Computer Vision papers:**

```python
search_query = "cat:cs.CV AND object detection"
```

## Troubleshooting

### Device Mismatch Error

If you get `RuntimeError: Expected all tensors to be on the same device...`:

- The code automatically handles device matching
- Embeddings are moved to the same device as the query tensor
- Ensure CUDA support is properly installed if using GPU

### Network Error: Cannot connect to ArXiv

- Check your internet connection
- Verify ArXiv API is not temporarily down (visit arxiv.org)
- The API may block too many requests - add longer delays in code

### Missing Database

If `paper_corpus.db` not found:

- Run `fetch_arxiv_papers.py` first to create and populate database
- Check that the script ran without errors

### No Results Found

- Verify database has content using `check_db.py`
- Check that embeddings file `embeddings.npy` exists
- Ensure query text is related to stored papers
- Increase `top_k` parameter in `test_search.py` to see more results

### Memory Issues with Large Corpus

- Reduce `max_results` in `fetch_arxiv_papers.py` to fetch fewer papers
- Consider processing papers in batches
- Increase chunk size (max_words) to reduce number of chunks

## Performance Notes

- **First Run:** 30-60 seconds (depends on network and number of papers)
- **Subsequent Runs:** <1 second for search (data is cached)
- **Embedding Generation:** ~0.1 seconds per chunk
- **Database Size:** ~5-10MB for 1000+ chunks

## Advanced Usage

### Searching Multiple Topics

Modify `fetch_arxiv_papers.py` to fetch papers on different topics:

```python
topics = ["machine learning", "deep learning", "computer vision"]

for topic in topics:
    papers = fetch_arxiv_papers(search_query=topic, max_results=3)
    # Process and store papers
```

### Adjusting Similarity Threshold

Modify `test_search.py` to filter results by minimum similarity:

```python
min_threshold = 0.7
filtered_results = [r for r in results if r['score'] > min_threshold]
```

### Custom Embeddings Model

To use a different SentenceTransformer model, modify `search.py` and `fetch_arxiv_papers.py`:

```python
# For faster embeddings (smaller model):
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# For better quality embeddings (larger model):
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# For domain-specific (scientific papers):
model = SentenceTransformer("sentence-transformers/allenai-specter")
```

## Comparison: Blog vs Research Papers Detector

| Aspect           | Blog Detector      | Research Papers Detector               |
| ---------------- | ------------------ | -------------------------------------- |
| Data Source      | Dev.to RSS Feed    | ArXiv API                              |
| Chunk Size       | 100 words          | 100 words                              |
| Metadata         | Title, URL         | Title, ArXiv ID, Authors               |
| Category Support | General tech blogs | Customizable (CS, Math, Physics, etc.) |
| API Key Required | No                 | No                                     |
| Rate Limiting    | Per-request delays | 2-3 second delays                      |

## Related Documentation

- See [Blog_Plag_detector.md](Blog_Plag_detector.md) for similar blog plagiarism detection
- For image captioning setup, see [INSTALLATION.md](INSTALLATION.md)
