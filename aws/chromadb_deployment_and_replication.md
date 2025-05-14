
# Deploying and Replicating ChromaDB

## Deployment Options

### 1. Docker (Single Node - for Dev)
Basic single-node instance using Docker:

```bash
docker run -d \
  -p 8000:8000 \
  --name chromadb \
  ghcr.io/chroma-core/chroma:latest
```

Access API at `http://localhost:8000`.

Optional environment variables:
- `IS_PERSISTENT=TRUE`
- `PERSIST_DIRECTORY=/path/to/store`

---

### 2. Python Package (In-Process, Local)
Great for embedding directly in Python apps:

```bash
pip install chromadb
```

```python
import chromadb
client = chromadb.Client()
```

**Note**: This is local and ephemeral by default unless configured for persistence.

---

### 3. Kubernetes (Recommended for Production)
Deploy ChromaDB behind a service, e.g., using Helm or Kustomize.

A simple K8s deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chromadb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chromadb
  template:
    metadata:
      labels:
        app: chromadb
    spec:
      containers:
      - name: chromadb
        image: ghcr.io/chroma-core/chroma:latest
        ports:
        - containerPort: 8000
        env:
        - name: IS_PERSISTENT
          value: "TRUE"
        - name: PERSIST_DIRECTORY
          value: "/data"
        volumeMounts:
        - mountPath: /data
          name: chromadb-storage
      volumes:
      - name: chromadb-storage
        persistentVolumeClaim:
          claimName: chromadb-pvc
```

Pair it with a `Service` and optionally `Ingress`.

---

## Replication Options

ChromaDB **does not natively support horizontal replication or clustering** yet. As of early 2025:

### 🔹 For HA/Replication:
You need to **wrap ChromaDB** with your own strategy:

1. **Read Replicas (Eventual Consistency)**:
   - Stand up multiple read-only ChromaDB instances from the same persistent volume (e.g., shared NFS, cloud volume snapshots).
   - Use a writer instance to ingest data and sync snapshots to read replicas.

2. **API Layer for Replication**:
   - Create a service that writes to multiple ChromaDB instances (like dual writes).
   - Use eventual consistency via a message queue (e.g., Kafka, SQS, Redis Streams).

3. **S3 Backend + CRON Syncing**:
   - Mount shared S3/GCS volume or sync local storage to S3.
   - Use a scheduled job to sync from the master to replicas.

4. **Use a Proxy (e.g., Envoy, HAProxy)**:
   - Front ChromaDB with a proxy that load-balances reads and directs writes to a single leader.

---

## 🛠 Alternatives If You Need Strong Replication
If you require high availability or true replication:
- **Weaviate**, **Qdrant**, or **Milvus** all support replication, sharding, and clustering out of the box.
- Consider these if you’re building a production vector search layer.

---

## TL;DR

| Feature       | Support           |
|---------------|-------------------|
| Native Replication | ❌ Not yet |
| Persistence        | ✅ Yes, via `IS_PERSISTENT` and `PERSIST_DIRECTORY` |
| Docker Support     | ✅ Yes |
| K8s Deployment     | ✅ Yes |
| Cloud-native replication | ❌ (Use external sync/proxy layer) |
