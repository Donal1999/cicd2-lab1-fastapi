from fastapi import FastAPI

app = FastAPI(title="Lab1 - FastAPI User Api")

@app.get("/health")
def health():
    return {"status": "ok"}