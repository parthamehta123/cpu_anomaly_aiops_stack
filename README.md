# CPU Anomaly AIOps Stack

This project is a minimal end-to-end AIOps demo with FastAPI, Prometheus metrics, CPU anomaly alerting, and drift retraining.

## Features
- FastAPI service with /healthz, /metrics, /predict endpoints
- Prometheus-compatible metrics
- CPU anomaly detection with 5-min threshold alerts
- Sample log file (cpu.jsonl) for testing
- Retrain-on-drift placeholder
- Docker + Kubernetes deployment

## Quickstart

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Test health:
```bash
curl http://localhost:8000/healthz
```

## CPU Alert Simulator

```bash
python cpu_alert.py
```

Feed it with sample data:
```bash
python -c "from cpu_alert import check_alert, stream; check_alert(stream(open('cpu.jsonl')))"
```

## Docker

```bash
docker build -t anomaly:v0.1.0 .
docker run -p 8000:8000 anomaly:v0.1.0
```

## Kubernetes

```bash
kubectl apply -f deploy.yaml
kubectl get pods
```

Service is exposed on port **8000**.
