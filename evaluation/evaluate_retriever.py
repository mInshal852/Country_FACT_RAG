# Runs evaluation
import json
import os
from configg import CHROMA_DB_PATH
from rag_pipeline.retriever import Retriever
from .retrieval_metrics import (
    precision_at_k,
    recall_at_k,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(PROJECT_ROOT, "evaluation", "retrieval_dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    dataset = load_dataset()
    retriever = Retriever(CHROMA_DB_PATH)

    precision_scores = {
        1: [],
        3: [],
        5: [],
    }
    recall_scores = {
        1: [],
        3: [],
        5: [],
    }

    print(f"Evaluating {len(dataset)} queries...\n")

    for sample in dataset:
        query = sample["query"]
        ground_truth = sample["relevant_chunks"]

        retrieved_chunks = retriever.retrieve(
            query=query,
            top_k=5,
        )

        retrieved_ids = [chunk["id"] for chunk in retrieved_chunks]

        for k in [1, 3, 5]:
            precision_scores[k].append(
                precision_at_k(
                    retrieved_ids,
                    ground_truth,
                    k,
                )
            )
            recall_scores[k].append(
                recall_at_k(
                    retrieved_ids,
                    ground_truth,
                    k,
                )
            )

    print("=" * 50)
    print("Retrieval Evaluation")
    print("=" * 50)
    print()
    print(f"Queries Evaluated : {len(dataset)}")
    print()

    for k in [1, 3, 5]:
        avg_precision = sum(precision_scores[k]) / len(precision_scores[k])
        avg_recall = sum(recall_scores[k]) / len(recall_scores[k])
        print(f"Precision@{k}: {avg_precision:.4f}")
        print(f"Recall@{k}:    {avg_recall:.4f}")
        print()


if __name__ == "__main__":
    main()
