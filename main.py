from fastapi import Fastapi

app = Fastapi()

@app.get("/")
def root() -> str:
    return "Merry Xmas, Di Gua Da Wang!"