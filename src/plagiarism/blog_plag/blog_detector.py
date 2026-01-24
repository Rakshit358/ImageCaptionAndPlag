from sentence_transformers import SentenceTransformer, util
import argparse
import json
import os


MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--caption', type=str, required=True, help='Caption text to check')
    parser.add_argument('--corpus', type=str, required=False, help='Path to a JSON file with corpus list')
    parser.add_argument('--threshold', type=float, default=0.75)
    args = parser.parse_args()

    model = SentenceTransformer(MODEL_NAME)

    input_text = args.caption
    print(f"Your input is : {input_text}")

    if args.corpus and os.path.exists(args.corpus):
        with open(args.corpus, 'r', encoding='utf-8') as f:
            corpus_texts = json.load(f)
    else:
        corpus_texts = [
            "A man riding a horse on a beach.",
            "A group of people playing soccer on a field.",
            "A dog jumping to catch a frisbee.",
            "A woman holding a baby in her arms.",
            "A person riding a skateboard down the street."
        ]

if __name__ == "__main__":
    main()