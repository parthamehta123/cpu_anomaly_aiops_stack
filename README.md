# CPU Anomaly AIOps Stack 🚀

This project deploys a **CPU anomaly detection and monitoring stack** on Kubernetes using:

- **FastAPI (Anomaly Service)** → exposes `/metrics` endpoint with CPU usage.
- **Prometheus Operator** → scrapes application metrics via `ServiceMonitor`.
- **Grafana** → visualizes CPU usage and anomalies.
- **PrometheusRules** → defines alerting rules for CPU anomalies.

---

## 📦 Components

### 1. **Anomaly Service**
- Runs as a Kubernetes **Deployment** with resource requests/limits.
- Exposes:
  - `/healthz` for liveness/readiness probes.
  - `/metrics` for Prometheus scraping.
- Service: `anomaly-service` (port `8000`).

### 2. **Prometheus Operator**
- Installed via Helm (`kube-prometheus-stack`).
- Provides:
  - `ServiceMonitor` CRDs for scraping metrics.
  - `PrometheusRule` CRDs for alerting.
  - Built-in node/pod monitoring.

### 3. **Grafana**
- Installed via Prometheus Operator.
- Port-forwarded locally:
  ```bash
  kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
  ```
- Default credentials:
  - Username: `admin`
  - Password: from secret:
    ```bash
    kubectl get secret monitoring-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode
    ```

### 4. **Prometheus Rules**
- Custom `PrometheusRule` deployed via:
  ```bash
  kubectl apply -f prometheus-rules.yaml
  ```
- Example: Trigger alert when CPU usage > 90% for 1m.

---

## ⚙️ Deployment Steps

1. **Deploy Anomaly Service**
   ```bash
   kubectl apply -f anomaly-deployment.yaml
   kubectl apply -f anomaly-service.yaml
   ```

2. **Verify Pods**
   ```bash
   kubectl get pods -l app=anomaly
   kubectl logs <anomaly-pod>
   ```

3. **Install Prometheus Operator**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
   ```

4. **Create ServiceMonitor**
   ```bash
   kubectl apply -f servicemonitor.yaml
   ```

5. **Create Alerts**
   ```bash
   kubectl apply -f prometheus-rules.yaml
   ```

6. **Access Grafana**
   ```bash
   kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
   ```

---

## 📊 Grafana Dashboard

- **Panel 1:** CPU Usage Percent per Pod  
  PromQL:
  ```promql
  cpu_usage_percent{pod=~".*anomaly.*"}
  ```

- **Panel 2:** Average CPU Usage (Namespace)  
  PromQL:
  ```promql
  avg(cpu_usage_percent) by (namespace)
  ```

- **Alerts:**  
  Highlight high CPU spikes > 90%.  

---

## ✅ Verification

- Run CPU stress test inside pod:
  ```bash
  kubectl exec -it <anomaly-pod> -- sh
  yes > /dev/null &
  ```
- Watch CPU spikes in Grafana (`CPU Anomaly Dashboard`).

---

## 🚀 Next Steps
- Add **alertmanager config** to send alerts (Slack/Email).
- Enable **Grafana variables** for pod/namespace filtering.
- Automate dashboard import with JSON configs.
