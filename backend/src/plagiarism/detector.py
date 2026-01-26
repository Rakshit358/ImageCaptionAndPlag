from sentence_transformers import SentenceTransformer, util
import argparse
import json
import os


MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


def build_corpus_embeddings(corpus_texts, model):
    corpus_emb = model.encode(corpus_texts, convert_to_tensor=True)
    return corpus_emb


def check_plagiarism(query_text, corpus_texts, corpus_emb, model, threshold=0.75):
    q_emb = model.encode(query_text, convert_to_tensor=True)
    sims = util.cos_sim(q_emb, corpus_emb)[0]
    best_score = float(sims.max())
    best_idx = int(sims.argmax())
    return {
        'score': best_score,
        'matched_text': corpus_texts[best_idx],
        'is_plagiarism': best_score >= threshold,
        'best_idx': best_idx
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--caption', type=str, required=True, help='Caption text to check')
    parser.add_argument('--corpus', type=str, required=False, help='Path to a JSON file with corpus list')
    parser.add_argument('--threshold', type=float, default=0.75)
    args = parser.parse_args()

    model = SentenceTransformer(MODEL_NAME)

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

    corpus_emb = build_corpus_embeddings(corpus_texts, model)
    res = check_plagiarism(args.caption, corpus_texts, corpus_emb, model, threshold=args.threshold)
    print('Result:', res)


if __name__ == "__main__":
    main()