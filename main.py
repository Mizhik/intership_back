from fastapi import FastAPI

app = FastAPI()


@app.get("/api/healthchecker")
def root():
    dict_result = {"status_code": 200, "detail": "ok", "result": "working"}
    return dict_result
