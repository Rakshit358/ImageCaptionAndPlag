
```markdown
##  Running the Flask API

Once the installation (INSTALLATION.md) is complete install flask (pip install flask), you can start the backend server:

python app.py

```

The server will default to `http://127.0.0.1:5000`.

---

### 🛠 API Endpoints & Working

All results are returned as JSON objects with text-based data.

#### 1. Plagiarism Detection

These endpoints automatically trigger a database creation/update script before running the similarity check.

| Category | Endpoint | Method |
| --- | --- | --- |
| **News** | `/test-news-plagiarism` | `POST` |
| **Blog** | `/test-blog-plagiarism` | `POST` |
| **Article** | `/test-article-plagiarism` | `POST` |

* **Payload:** `{"query": "Your text content here"}`
* **Working:** The system calls the respective `run_db_creation` script to index current records and then uses `run_test_plagiarism` to return a similarity match.

#### 2. Image Captioning

* **Endpoint:** `/generate-caption`
* **Method:** `POST`
* **Input:** Image file (multipart/form-data, key: `image`)
* **Working:**
1. Loads the pre-trained model via `load_model`.
2. Detects if a GPU is available (`cuda`) or falls back to `cpu`.
3. Processes the image and generates a descriptive text string.



---

### 📊 Output Format

**Image Caption Example**

```json
{
  "caption": "A mountain landscape under a clear blue sky"
}

```

**Plagiarism Result Example**

```json
{
  "similarity_score": 0.92,
  "top_matches": [
    {
      "source": "Article Name",
      "score": 0.92
    }
  ]
}

```

Here is the updated section formatted for Postman instead of cURL. You can replace the "Testing with cURL" section in your markdown file with this.

```markdown
### 🧪 Testing with Postman

You can test the endpoints using [Postman](https://www.postman.com/) by following these steps:

#### 1. Test Plagiarism Detection

* **Method:** `POST`
* **URL:** `http://127.0.0.1:5000/test-news-plagiarism`
* **Body Configuration:**
    1.  Go to the **Body** tab.
    2.  Select **raw**.
    3.  Change the dropdown from `Text` to **JSON**.
    4.  Paste the following JSON payload:

```json
{
    "query": "Enter text to check here"
}

```

#### 2. Test Image Captioning

* **Method:** `POST`
* **URL:** `http://127.0.0.1:5000/generate-caption`
* **Body Configuration:**
1. Go to the **Body** tab.
2. Select **form-data**.
3. In the **Key** column, type `image`.
4. Hover over the `image` key cell and change the type from **Text** to **File** (via the small dropdown arrow that appears).
5. In the **Value** column, click **Select File** and upload your `.jpg` or `.png` image.


