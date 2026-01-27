from flask import Flask, jsonify, request
from scripts.run_detector import (
    run_news_db_creation,
    run_blog_db_creation,
    run_article_db_creation,
    run_test_news_plagiarism,
    run_test_blog_plagiarism,
    run_test_article_plagiarism
)
from PIL import Image
import torch
from src.captioning.generate import load_model, caption_image



app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask backend running "})


# ---------------- NEWS PLAGIARISM ----------------
@app.route("/test-news-plagiarism", methods=["POST"])
def test_news_plagiarism():
    data = request.get_json(force=True)
    query = data.get("query")

    # CREATING THE DB
    run_news_db_creation()

    # Testing similarity score of the query over news
    result = run_test_news_plagiarism(query)
    return jsonify(result)


# ---------------- BLOG PLAGIARISM ----------------
@app.route("/test-blog-plagiarism", methods=["POST"])
def test_blog_plagiarism():
    data = request.get_json(force=True)
    query = data.get("query")

    # CREATING THE DB (if required for blogs)
    run_blog_db_creation()

    # Testing similarity score of the query over blogs
    result = run_test_blog_plagiarism(query)
    return jsonify(result)


# ---------------- ARTICLE PLAGIARISM ----------------
@app.route("/test-article-plagiarism", methods=["POST"])
def test_article_plagiarism():
    data = request.get_json(force=True)
    query = data.get("query")

    # CREATING THE DB (if required for articles)
    run_article_db_creation()

    # Testing similarity score of the query over articles
    result = run_test_article_plagiarism(query)
    return jsonify(result)



# ----------------Image Caption generator----------------


@app.route("/generate-caption", methods=["POST"])
def generate_caption():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor, model = load_model(device)

    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]  # FileStorage object
    image = Image.open(file.stream)

    caption = caption_image(processor, model, image, device)
    return jsonify({"caption": caption})

if __name__ == "__main__":
    app.run(debug=True)
