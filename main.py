from fastapi import FastAPI

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    return {"status_code": 200, "detail": "ok", "result": "working"}
