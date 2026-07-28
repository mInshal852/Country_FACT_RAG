from fastapi import FastAPI
from backend.api.routers.health import router as health_router
from backend.api.routers.ask import router as ask_router
from backend.api.routers.retrieve import router as retrieve_router
from backend.api.routers.decompose import router as decompose_router
from backend.api.core.logging_config import setup_logging
from backend.api.core.exception_handler import register_exception_handlers

setup_logging()

app = FastAPI(
    title="Country FACT RAG API",
    description="A Retrieval-Augmented Generation (RAG) API for answering country-related questions.",
    version="1.0.0",
)

register_exception_handlers(
    app
)  # global exception handler, want to learn about see the notes in api/core
app.include_router(health_router)
app.include_router(ask_router)
app.include_router(retrieve_router)
app.include_router(decompose_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Country FACT RAG API!"}


# decorator in fastAPI, note: In FastAPI, decorators connect a URL and an HTTP method (GET, POST, PUT, DELETE) to a Python function, so FastAPI knows which function to run when a request arrives.
