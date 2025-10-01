from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import PlainTextResponse

app = FastAPI()

REQUEST_COUNT = Counter("request_count", "Total request count")


@app.get("/")
def root():
    return {"service": "CPU Anomaly AIOps Stack", "status": "running"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest().decode("utf-8")


@app.get("/predict")
def predict(x: int):
    REQUEST_COUNT.inc()
    return {"input": x, "prediction": x * 2}
