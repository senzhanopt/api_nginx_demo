from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index() -> str:
    return "Hello, Welcome!"

@app.get("/health")
def health_check() -> dict:
    return {"status": "OK"}