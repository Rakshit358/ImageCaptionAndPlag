# Blog Plagiarism Detector - Setup & Execution Guide

## Architecture Flow

```
User Text
↓
Light Preprocessing
↓
Semantic Embedding (SentenceTransformer)
↓
Vector Search (Primary signal)
↓
Top-K candidate blog chunks
↓
Optional Keyword/Core-Idea validation
↓
Plagiarism decision + sources
```

## Prerequisites & Installation

### Step 1: Install Required Dependencies

```bash
pip install feedparser requests beautifulsoup4 sentence-transformers numpy torch sqlite3
```

### Step 2: Navigate to Project Directory

```bash
cd src/plagiarism/blog_plag
```

## Running the Blog Detector

### Step 1: Initialize Database & Fetch Blogs

Run this first to populate the blog corpus with embeddings:

```bash
python fetch_test_blogs.py
```

**What this does:**

- Creates SQLite database (`blog_corpus.db`)
- Fetches sample blogs from Dev.to RSS feed
- Extracts and cleans blog content
- Splits text into 100-word chunks
- Generates semantic embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores chunks and embeddings for later search

### Step 2: Verify Database Contents (Optional)

Check if the database was populated correctly:

```bash
python check_db.py
```

**What this does:**

- Shows total number of chunks in database
- Displays sample entries and their sources

### Step 3: Test Plagiarism Search

Run semantic similarity search on stored blog corpus:

```bash
python test_search.py
```

**What this does:**

- Takes a predefined query text
- Searches the blog corpus using cosine similarity
- Returns top-3 matching blog chunks with similarity scores
- Shows source URLs where matches were found

## Project Files Overview

| File                  | Purpose                                                                 |
| --------------------- | ----------------------------------------------------------------------- |
| `fetch_test_blogs.py` | **Entry point** - Fetches blogs, creates embeddings, populates database |
| `storage.py`          | Database operations (init, insert chunks, save/load embeddings)         |
| `search.py`           | Core search logic using semantic similarity (cosine distance)           |
| `check_db.py`         | Utility to inspect database contents                                    |
| `test_search.py`      | Test script to query the plagiarism detector                            |
| `embeddings.npy`      | Pre-computed embeddings file (auto-generated)                           |
| `blog_corpus.db`      | SQLite database storing blog chunks (auto-generated)                    |

## Complete Workflow Example

```bash
# 1. Setup and populate corpus
python fetch_test_blogs.py

# 2. Verify data was stored
python check_db.py

# 3. Test plagiarism detection
python test_search.py
```

## Key Components

### Embedding Model

- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Purpose:** Converts text chunks into 384-dimensional semantic vectors
- **Why:** Enables semantic similarity search beyond keyword matching

### Search Method

- **Algorithm:** Cosine Similarity
- **Process:** Compares query embedding against all stored embeddings
- **Output:** Top-K most similar blog chunks with similarity scores (0-1)

## Troubleshooting

### Device Mismatch Error

If you get `RuntimeError: Expected all tensors to be on the same device...`:

- The embeddings are being moved to match the query device automatically
- Ensure CUDA support is properly installed if using GPU

### Missing Database

If `blog_corpus.db` not found:

- Run `fetch_test_blogs.py` first to create and populate the database

### No Results Found

- Verify database has content with `check_db.py`
- Check similarity threshold (default: 0.75)
- Ensure model is properly downloaded by sentence-transformers
