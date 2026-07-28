# Runs evaluation
import json
import os
from backend.configg import CHROMA_DB_PATH
from backend.rag_pipeline.inference.a4_retriever import Retriever
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


# # READ IT (IMP):
# Retrieval Evaluation Dataset

# In my project, I first take one chunk from the dataset and give it to the LLM. The LLM generates questions only from that chunk, not from the whole document. Since I know which chunk was used to create the question, I also know that this chunk is the correct answer. Therefore, each query in my dataset has only one relevant_chunk. This is called chunk-level retrieval evaluation because I am checking whether the retriever can find the same chunk that was used to generate the question.

# In real-world or industry datasets, questions are usually broader and may require information from multiple chunks. For example, the question "Explain Germany's culture" may need information from chunks about food, music, literature, traditions, and architecture. Therefore, these datasets store multiple relevant_chunks for a single query. The goal is to check whether the retriever can find all the important chunks needed to answer the question.

# Note: Since my dataset has only one relevant_chunk for each query, both Recall and Precision are easier to calculate and interpret. If the retriever finds the correct chunk, Recall = 1.0; otherwise, Recall = 0.0. This does not mean recall is always high—it only means there is only one correct chunk to find. Precision still depends on how many chunks are retrieved. For example, if I retrieve the top 5 chunks and only 1 is the correct chunk, then Precision@5 = 1/5 = 0.20. If I retrieve only the correct chunk, then Precision@1 = 1/1 = 1.0. In industry datasets, where a query can have multiple relevant chunks, both Recall and Precision provide a more detailed evaluation because the retriever is expected to find several relevant chunks instead of just one.

# output:
# pyenv) inshal@inshalR:~/Documents/RAG_Projects/CountryFact_Rag/Country_FACT_RAG$ python -m evaluation.evaluate_retriever
# Evaluating 1032 queries...

# ==================================================
# Retrieval Evaluation
# ==================================================

# Queries Evaluated : 1032

# Precision@1: 0.6502
# Recall@1:    0.6502

# Precision@3: 0.2846
# Recall@3:    0.8537

# Precision@5: 0.1806
# Recall@5:    0.9031
