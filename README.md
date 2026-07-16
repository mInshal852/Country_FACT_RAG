# CountryFacts-RAG

A lightweight retrieval-augmented generation scaffold for country facts.

## Structure

- `datasets/raw/` stores source HTML pages.
- `datasets/processed/` stores cleaned text files.
- `dataset_pipeline/` contains the dataset build steps.
- `rag_pipeline/` contains loading, chunking, embedding, retrieval, and generation helpers.
- `ui/` contains the Streamlit app.
- `api/` contains the FastAPI app.
- `tests/` contains basic checks for the pipeline.

## Setup

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Populate `.env` with any required API keys or model settings.
4. Run the dataset pipeline to build processed text files.
5. Start the UI or API entrypoint.

## Notes

This repository is scaffolded so each folder and file exists and can be extended with real scraping, parsing, retrieval, and generation logic.
