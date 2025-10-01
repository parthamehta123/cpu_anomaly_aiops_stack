from fastapi import FastAPI
from prometheus_client import Counter, Gauge, generate_latest
from fastapi.responses import PlainTextResponse
import psutil

app = FastAPI()

# Custom metrics
REQUEST_COUNT = Counter("request_count", "Total request count")
CPU_USAGE = Gauge("cpu_usage_percent", "Current CPU usage percentage")


@app.get("/")
def root():
    return {"service": "CPU Anomaly AIOps Stack", "status": "running"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    # Update CPU usage gauge before returning metrics
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    return generate_latest().decode("utf-8")


@app.get("/predict")
def predict(x: int):
    REQUEST_COUNT.inc()
    return {"input": x, "prediction": x * 2}
