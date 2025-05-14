# Deploy Ollama with a Model for Production

## Overview

**Ollama** allows you to run LLMs (like LLaMA, Mistral, etc.) locally with GPU support. For production use, you’ll need:

1. Infrastructure (bare metal or cloud VM with GPU)
2. Ollama installed
3. Model pulled and loaded
4. Reverse proxy (for HTTPS, logging, and load balancing)
5. (Optional) Kubernetes for orchestration
6. Secure access (auth, rate limiting)

---

## 1. Infrastructure Requirements

**Minimum recommended production specs** (depends on model):

- **GPU**: NVIDIA with CUDA support (e.g., A100, V100, or even 3090)
- **RAM**: 32–64 GB+
- **Disk**: SSD, 20–100 GB depending on model size
- **OS**: Ubuntu 20.04+, Docker compatible

💡 You can use:
- **Bare metal** (for cost efficiency)
- **Cloud VM** (e.g., AWS EC2 g5, Google Cloud A2-highgpu, etc.)

---

##  2. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Or via Docker:

```bash
docker run --gpus all -d -p 11434:11434 ollama/ollama
```

---

## 3. Load a Model

To pull and start a model:

```bash
ollama pull mistral
ollama run mistral
```

In production, you can preload the model via script:

```bash
ollama run mistral --model-path /models/mistral
```

---

## 4. Expose via Reverse Proxy (e.g., NGINX + HTTPS)

Example NGINX config (with HTTPS via certbot):

```nginx
server {
    listen 443 ssl;
    server_name llm.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/llm.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/llm.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then use certbot:

```bash
sudo certbot --nginx -d llm.yourdomain.com
```

---

## 5. Secure the Endpoint

- Use **API gateway** (e.g., Kong, NGINX, or Cloudflare Tunnel) for:
  - **Rate limiting**
  - **IP whitelisting**
  - **Auth (API Key, OAuth2)**
- Optionally isolate via **private VPC** and only expose via reverse proxy
- Log & monitor usage with Prometheus/Grafana or external services

---

## 6. Optional: Kubernetes Deployment

You can containerize and deploy Ollama in **Kubernetes** with GPU scheduling:

**Sample Helm-free manifest (simplified):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama
        ports:
        - containerPort: 11434
        resources:
          limits:
            nvidia.com/gpu: 1
      nodeSelector:
        kubernetes.io/arch: amd64
```

Use a **Service** and **Ingress** with cert-manager for HTTPS.

---

## Optional Enhancements

- **Autoscaling**: Horizontal Pod Autoscaler (HPA) based on load
- **Model hot-swapping**: Run Ollama behind a facade service that can switch models
- **Logging**: Centralize logs with Loki or Elastic stack
- **Auth**: Use JWT or API gateway

---

## Health Check & Test

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Say hello to production."
}'
```
