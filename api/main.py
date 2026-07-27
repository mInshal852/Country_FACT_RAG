from fastapi import FastAPI
from api.routers.health import router as health_router
from api.routers.ask import router as ask_router

app = FastAPI(
    title="Country FACT RAG API",
    description="A Retrieval-Augmented Generation (RAG) API for answering country-related questions.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(ask_router)


@app.get("/")
def root():
    return {"message": "Welcome to the Country FACT RAG API!"}


# decorator in fastAPI, note: In FastAPI, decorators connect a URL and an HTTP method (GET, POST, PUT, DELETE) to a Python function, so FastAPI knows which function to run when a request arrives.
