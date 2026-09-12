from fastapi import FastAPI

app = FastAPI(
    title="Permission-Aware RAG",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Permission-Aware RAG API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }