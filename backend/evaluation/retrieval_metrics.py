# Precision@k, Recall@k

"""
retrieval_metrics.py

Evaluation metrics for semantic retrieval.
"""


def precision_at_k(retrieved_ids, relevant_ids, k):
    """
    Computes Precision@K.

    Args:
        retrieved_ids (list): Retrieved chunk IDs ranked by relevance.
        relevant_ids (list): Ground truth relevant chunk IDs.
        k (int): Number of top retrieved chunks to consider.

    Returns:
        float
    """
    if k == 0:
        return 0.0

    retrieved_k = retrieved_ids[:k]

    relevant_retrieved = sum(chunk_id in relevant_ids for chunk_id in retrieved_k)

    return relevant_retrieved / k


def recall_at_k(retrieved_ids, relevant_ids, k):
    """
    Computes Recall@K.

    Args:
        retrieved_ids (list): Retrieved chunk IDs ranked by relevance.
        relevant_ids (list): Ground truth relevant chunk IDs.
        k (int): Number of top retrieved chunks to consider.

    Returns:
        float
    """

    if len(relevant_ids) == 0:
        return 0.0

    retrieved_k = retrieved_ids[:k]

    relevant_retrieved = sum(chunk_id in relevant_ids for chunk_id in retrieved_k)

    return relevant_retrieved / len(relevant_ids)
