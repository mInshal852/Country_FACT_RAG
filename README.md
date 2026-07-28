# 🌍 Country FACT RAG

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

A production-style **Retrieval-Augmented Generation (RAG)** application that answers country-related questions using semantic search over a curated knowledge base built from **Britannica** articles.

The project demonstrates an end-to-end RAG pipeline, including dataset creation, document preprocessing, vector indexing, semantic retrieval, query decomposition, prompt construction, LLM-based answer generation, a **FastAPI backend**, a **Streamlit frontend**, and **Dockerized deployment**.

---

# ✨ Features

- 🌍 Country Question Answering
- 🔍 Semantic Retrieval using ChromaDB
- 🧠 Sentence Transformer Embeddings (`all-MiniLM-L6-v2`)
- ✍️ Query Decomposition for Multi-Country Queries
- 📦 Batch Retrieval with Duplicate Removal
- 🤖 LLM-based Answer Generation via OpenRouter
- 📝 Prompt Builder
- 📊 Retrieval Evaluation (Precision@K & Recall@K)
- ⚙️ Configurable LLM Models
- 🚀 FastAPI REST API
- 💬 Streamlit Chat Interface
- 🐳 Dockerized Backend
- 🐳 Dockerized Frontend
- 🐳 Docker Compose Support
- 🏗️ Modular Project Architecture

---

# 🏗️ System Architecture

```text
                    User
                      │
                      ▼
          Streamlit Frontend (UI)
                      │
             HTTP Request (/ask)
                      │
                      ▼
              FastAPI Backend
                      │
                      ▼
          Query Decomposition LLM
                      │
                      ▼
     Sentence Transformer Embeddings
                      │
                      ▼
              ChromaDB Vector DB
                      │
           Retrieve Top-K Chunks
                      │
          Duplicate Chunk Removal
                      │
                      ▼
             Prompt Construction
                      │
                      ▼
            OpenRouter LLM (Qwen)
                      │
                      ▼
              Generated Response
```

---

# 📂 Project Structure

```text
Country_FACT_RAG/
│
├── backend/
│   ├── api/                    # FastAPI application
│   ├── rag_pipeline/           # RAG implementation
│   ├── datasets/              # Knowledge base
│   ├── vectordb/              # ChromaDB persistence
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py                 # Streamlit application
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
├── LICENSE
└── .gitignore
```

---

# 📊 Dataset Structure

```text
datasets/
│
├── raw/          # Raw scraped HTML pages
├── processed/    # Cleaned JSON files
├── txt/          # Plain text documents
├── chunks/       # Chunked documents
└── datalinks/    # Source metadata
```

---

# 🔄 System Workflow

## Offline Indexing Pipeline

1. Scrape country articles from Britannica.
2. Parse HTML pages.
3. Generate cleaned JSON files.
4. Convert documents into plain text.
5. Split documents into chunks.
6. Generate embeddings.
7. Store embeddings inside ChromaDB.

---

## Online Query Pipeline

1. User submits a question.
2. Query Decomposer rewrites or splits complex queries.
3. Generate embeddings for each query.
4. Retrieve Top-K relevant chunks from ChromaDB.
5. Remove duplicate chunks.
6. Build the final prompt.
7. Generate the answer using the LLM.
8. Return the response through the FastAPI API.
9. Display the answer in the Streamlit interface.

---

# ⚙️ Vector Database Configuration

| Component | Configuration |
|-----------|---------------|
| Vector Database | ChromaDB |
| ANN Index | HNSW |
| Similarity Metric | Cosine Similarity |
| Embedding Model | all-MiniLM-L6-v2 |

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| Frontend | Streamlit |
| Vector Database | ChromaDB |
| Embedding Model | all-MiniLM-L6-v2 |
| LLM | Qwen (OpenRouter) |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Version Control | Git & GitHub |

---

# 📈 Evaluation

Current retrieval performance:

| Metric | Score |
|---------|------:|
| Precision@1 | 0.6502 |
| Recall@1 | 0.6502 |
| Precision@3 | 0.2846 |
| Recall@3 | 0.8537 |
| Precision@5 | 0.1806 |
| Recall@5 | 0.9031 |

---

# 🚀 Installation

## Clone the Repository

```bash
git clone https://github.com/<your-username>/Country_FACT_RAG.git

cd Country_FACT_RAG
```

---

## Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv pyenv
source pyenv/bin/activate
```

### Windows

```bash
python -m venv pyenv

pyenv\Scripts\activate
```

---

## Install Dependencies

Backend

```bash
cd backend

pip install -r requirements.txt
```

Frontend

```bash
cd ../frontend

pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create:

```text
backend/.env
```

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key

DECOMPOSITION_MODEL=qwen/qwen3-8b
GENERATOR_MODEL=qwen/qwen3-14b
```

---

# ▶️ Running the Project (Without Docker)

## Start the FastAPI Backend

```bash
cd backend

uvicorn api.main:app --reload
```

Backend API

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## Start the Streamlit Frontend

```bash
cd frontend

streamlit run app.py
```

Frontend

```
http://localhost:8501
```

---

# 🐳 Running with Docker

Build and start both the frontend and backend containers:

```bash
docker compose up --build
```

Once the containers are running:

Frontend

```
http://localhost:8501
```

Backend

```
http://localhost:8000/docs
```

To stop the containers:

```bash
docker compose down
```

---

# 💬 Example Queries

- What is the capital of Pakistan?
- Tell me about Germany's government.
- Compare Japan and Malaysia.
- What are the capitals of Pakistan, Germany, and Saudi Arabia?
- Which country has a constitutional monarchy?
- Tell me about the geography of Saudi Arabia.
- Compare Pakistan, China, and Japan.

---

# 📸 Screenshots

## Home Page

> Add screenshot here

---

## Chat Interface

> Add screenshot here

---

## Swagger API

> Add screenshot here

---

# 📚 Learning Outcomes

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- ChromaDB
- Sentence Transformers
- Query Decomposition
- Prompt Engineering
- FastAPI
- REST APIs
- Streamlit
- Docker
- Docker Compose
- OpenRouter LLM Integration

---

# 🚀 Future Improvements

- Hybrid Retrieval (BM25 + Dense Retrieval)
- Cross-Encoder Re-ranking
- Metadata Filtering
- Source Citations
- Conversation Memory
- Streaming Responses
- Multi-language Support
- Phoenix Observability
- RAGAS / DeepEval Evaluation
- Authentication & User Management

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

If you have ideas to improve the project, feel free to fork the repository and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Muhammad Inshal**
