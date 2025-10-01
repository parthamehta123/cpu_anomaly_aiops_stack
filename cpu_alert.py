from datetime import datetime, timedelta
import json
import requests

THRESHOLD = 90
WINDOW = timedelta(minutes=5)
METRICS_URL = "http://localhost:8000/metrics"


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def stream(records):
    """Yield parsed records from a JSONL stream."""
    for line in records:
        if line.strip():
            yield json.loads(line)


def check_alert(records):
    high_start, last_high_ts = None, None
    for rec in records:
        ts = parse_ts(rec["timestamp"])
        cpu = float(rec.get("cpu", 0))
        if cpu > THRESHOLD:
            if high_start is None:
                high_start = ts
            last_high_ts = ts
            if last_high_ts - high_start >= WINDOW:
                print(f"ALERT: CPU > {THRESHOLD}% for 5+ minutes at {ts.isoformat()}")
                _push_metric(cpu)
        else:
            if high_start and last_high_ts - high_start >= WINDOW:
                print(
                    f"ALERT: CPU > {THRESHOLD}% for 5+ minutes before dropping at {ts.isoformat()}"
                )
                _push_metric(cpu)
            high_start, last_high_ts = None, None

    # Handle if still high at end of stream
    if high_start and last_high_ts - high_start >= WINDOW:
        print(
            f"ALERT: CPU > {THRESHOLD}% for 5+ minutes until stream end at {last_high_ts.isoformat()}"
        )
        _push_metric(cpu)


def _push_metric(cpu: float):
    """Simulate reporting by pinging the FastAPI /metrics endpoint."""
    try:
        resp = requests.get(METRICS_URL, timeout=5)
        if resp.status_code == 200:
            print(f"✅ Reported CPU={cpu} to metrics endpoint")
        else:
            print(f"⚠️ Metrics endpoint returned {resp.status_code}")
    except Exception as e:
        print(f"❌ Failed to contact metrics endpoint: {e}")
