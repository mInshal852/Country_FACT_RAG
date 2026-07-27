# 🌍 Country FACT RAG

A Retrieval-Augmented Generation (RAG) system that answers country-related questions using semantic search over a custom knowledge base built from Britannica articles.

The project includes a complete pipeline for scraping, processing, chunking, indexing, retrieving, and generating answers using Large Language Models (LLMs).

---

## Features

- Semantic Retrieval using ChromaDB
- Sentence Transformer Embeddings (`all-MiniLM-L6-v2`)
- Query Decomposition for multi-country queries
- Batch Retrieval with duplicate removal
- Prompt Builder
- LLM-based Answer Generation
- Retrieval Evaluation (Precision@K & Recall@K)
- Configurable LLM models
- Modular project architecture

---

## Project Structure

```text
Country_FACT_RAG/
│
├── api/                     # FastAPI application
├── ui/                      # Streamlit application
│
├── dataset_pipeline/        # Dataset creation pipeline
│
├── datasets/
│   ├── raw/                 # Raw scraped HTML files
│   ├── processed/           # Cleaned JSON files
│   ├── txt/                 # Plain text documents
│   ├── chunks/              # Chunked documents
│   └── datalinks/           # Source metadata
│
├── evaluation/              # Retrieval evaluation
│
├── rag_pipeline/
│   ├── indexing/
│   └── inference/
│
├── tests/
├── vectordb/
│
├── config.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Dataset Structure

- `datasets/raw/` stores the raw scraped HTML pages.
- `datasets/processed/` stores cleaned JSON documents.
- `datasets/txt/` stores plain text documents.
- `datasets/chunks/` stores chunked documents for embedding.
- `datasets/datalinks/` stores metadata and source links.

---

## Pipeline Overview

### Offline Indexing Pipeline

1. Scrape country articles.
2. Parse HTML pages.
3. Generate cleaned JSON files.
4. Convert documents into plain text.
5. Split documents into chunks.
6. Generate embeddings.
7. Store embeddings in ChromaDB.

### Online Query Pipeline

1. User submits a query.
2. Query Decomposer splits complex queries (if necessary).
3. Generate embeddings for each query.
4. Retrieve Top-K relevant chunks from ChromaDB.
5. Merge duplicate chunks.
6. Build the final prompt.
7. Generate the answer using the LLM.

---

## Vector Database Configuration

| Component | Configuration |
|-----------|---------------|
| Vector Database | ChromaDB |
| ANN Index | HNSW |
| Distance Metric | Cosine Similarity |
| Embedding Model | all-MiniLM-L6-v2 |

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Qwen3 (OpenRouter) |
| API | FastAPI |
| UI | Streamlit |

---

## Evaluation

Current retrieval performance:

| Metric | Score |
|---------|-------|
| Precision@1 | 0.6502 |
| Recall@1 | 0.6502 |
| Precision@3 | 0.2846 |
| Recall@3 | 0.8537 |
| Precision@5 | 0.1806 |
| Recall@5 | 0.9031 |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/Country_FACT_RAG.git

cd Country_FACT_RAG
```

Create a virtual environment:

```bash
python -m venv pyenv
```

Activate it:

**Linux/macOS**

```bash
source pyenv/bin/activate
```

**Windows**

```bash
pyenv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add the required API keys and model configuration.

Example:

```env
OPENROUTER_API_KEY=your_api_key
```
```configg.py
DECOMPOSITION_MODEL=qwen/qwen3-8b
GENERATOR_MODEL=qwen/qwen3-14b
```

---

## Running the Project

### Build the Dataset & Vector Database

```bash
python dataset_pipeline/main.py
```

### Start the Streamlit Application

```bash
streamlit run ui/app.py
```

### Start the FastAPI Server

```bash
uvicorn api.main:app --reload
```

---

## Example Queries

- What is the capital of Pakistan?
- Tell me about Germany's government.
- Compare Japan and Malaysia.
- What are the capitals of Pakistan, Germany, and Saudi Arabia?
- Which country has a constitutional monarchy?

---

## Future Improvements

- Source citations
- Hybrid Retrieval
- Re-ranking
- Docker support
- Phoenix Observability
- Answer Evaluation (RAGAS / DeepEval)

---

## License

This project is licensed under the MIT License.