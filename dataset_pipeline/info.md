# Dataset Pipeline Notes

## Problem Faced

While building the dataset pipeline, we initially attempted to scrape country information directly from **Britannica** using the `requests` library.

However, every request returned a **403 Forbidden** response because Britannica is protected by advanced anti-bot mechanisms. Even after adding browser-like headers (`User-Agent`), the website continued to block automated requests.

## Solution

To overcome this issue, we decided to use the **Zyte API**.

Zyte acts as an intermediary between our application and the target website. Instead of our scraper directly requesting Britannica, the request is sent to Zyte, which fetches the webpage using its browser rendering and anti-bot infrastructure, then returns the HTML content to our application.

### Workflow

```text
Scraper
    │
    ▼
Zyte API
    │
    ▼
Britannica
    │
    ▼
HTML Response
    │
    ▼
Our Dataset Pipeline
```

---

## Pricing

We selected the **Pay as you go** plan.

### How it works

- No monthly commitment.
- Pay only for the requests you actually make.
- Pricing is calculated **per 1,000 requests**, not by purchasing a package of 1,000 requests.
- The cost of each request depends on the target website and whether Zyte needs browser rendering or advanced anti-bot handling.

### Example

Suppose the request price is:

```text
$0.13 per 1,000 requests
```

Then:

| Requests | Approximate Cost |
|----------:|-----------------:|
| 1 | $0.00013 |
| 10 | $0.0013 |
| 100 | $0.013 |
| 1,000 | $0.13 |

> **Note:** The actual cost may vary depending on the website and request type (HTTP request vs Browser Rendering). Always check Zyte's Pricing Calculator for the latest pricing.

---

## Why Zyte?

- Handles anti-bot protection.
- Supports browser rendering.
- Eliminates the need to manage proxies.
- Eliminates the need to manage browser automation.
- Provides a simple API for fetching web pages.
- Returns clean HTML that can be processed by our dataset pipeline.

---

## Why We Chose Zyte

Our goal is to learn and build a high-quality **Retrieval-Augmented Generation (RAG)** system—not to spend days bypassing website bot protection.

Using Zyte allows us to focus on the core components of the project:

- Dataset Generation
- HTML Parsing
- Section Extraction
- LLM Cleaning
- Chunking
- Embeddings
- ChromaDB
- Semantic Retrieval
- Answer Generation

This keeps the project focused on AI engineering rather than web scraping challenges.