# Dockerfile for Music Freshness CAG
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for CAG
RUN pip install --no-cache-dir etcd3 chromadb sentence-transformers

# Copy the code
COPY utils/ utils/
COPY fresh/ fresh/

# Set environment variables for etcd (can be overridden)
ENV ETCD_HOST=etcd ETCD_PORT=2379

ENTRYPOINT ["python", "fresh/music_freshness_cag.py"] 