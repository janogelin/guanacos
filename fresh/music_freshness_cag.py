"""
music_freshness_cag.py

A Content-Aware Gatherer (CAG) for music freshness, following the workflow in AiDocs/how_to_create_music_freshness_cag.txt.

Features:
- Crawl top music news sites with thread limiting using etcd
- Use the PageCrawler module to fetch and parse web pages
- Extract embeddings from crawled content using sentence-transformers
- Store embeddings in a local Chroma vector database
- Provide a query interface to retrieve relevant context
- Designed for Docker compatibility

Dependencies:
- requests
- beautifulsoup4
- etcd3
- sentence-transformers
- chromadb

Usage:
    python fresh/music_freshness_cag.py

Docker:
    # Example Dockerfile usage:
    # docker build -t music-freshness-cag .
    # docker run --rm music-freshness-cag
"""

import os
import uuid
import json
import time
import etcd3
import chromadb
from sentence_transformers import SentenceTransformer
from urllib.parse import urlparse
from threading import Thread
import subprocess
import importlib.util
import pathlib
import requests
import sys

# Configuration
TOP_SITES = [
    "https://www.billboard.com/",
    "https://pitchfork.com/",
    "https://www.rollingstone.com/",
    "https://www.nme.com/"
]
THREAD_LIMIT = 5
ETCD_HOST = os.environ.get("ETCD_HOST", "localhost")
ETCD_PORT = int(os.environ.get("ETCD_PORT", 2379))
CRAWL_OUTPUT_DIR = "fresh/crawled_json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_COLLECTION = "music_freshness"
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:4b")

os.makedirs(CRAWL_OUTPUT_DIR, exist_ok=True)

def safe_etcd_client(host, port):
    try:
        client = etcd3.client(host=host, port=port)
        # Test connection
        list(client.status().items())
        return client
    except Exception as e:
        print(f"[ERROR] Could not connect to etcd at {host}:{port}. Is etcd running and accessible?\nError: {e}")
        sys.exit(1)

# Initialize etcd client
etcd = safe_etcd_client(ETCD_HOST, ETCD_PORT)

# Initialize embedding model and Chroma DB
embedder = SentenceTransformer(EMBEDDING_MODEL)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)

utils_path = pathlib.Path(__file__).parent.parent / 'utils' / 'page_crawler.py'
spec = importlib.util.spec_from_file_location('page_crawler', str(utils_path))
page_crawler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(page_crawler)
PageCrawler = page_crawler.PageCrawler

crawler = PageCrawler()

def get_domain(url):
    return urlparse(url).netloc.replace('www.', '')

def acquire_thread_slot(domain):
    """Acquire a thread slot for a domain using etcd semaphores."""
    prefix = f"/crawler/semaphores/{domain}/"
    keys = list(etcd.get_prefix(prefix, keys_only=True))
    if len(keys) < THREAD_LIMIT:
        lease = etcd.lease(300)  # 5 minutes
        thread_id = str(uuid.uuid4())
        key = f"{prefix}thread-{thread_id}"
        etcd.put(key, "", lease=lease)
        return key, lease
    return None, None

def release_thread_slot(key, lease):
    if key:
        etcd.delete(key)
        if lease:
            lease.revoke()

def crawl_and_store(url):
    domain = get_domain(url)
    key, lease = None, None
    try:
        # Acquire thread slot
        while True:
            key, lease = acquire_thread_slot(domain)
            if key:
                break
            print(f"Thread limit reached for {domain}, waiting...")
            time.sleep(2)
        # Crawl and save
        output_file = os.path.join(CRAWL_OUTPUT_DIR, f"{domain}.json")
        print(f"Crawling {url} -> {output_file}")
        crawler.crawl_and_save(url, output_file)
    finally:
        release_thread_slot(key, lease)

def extract_and_store_embeddings():
    """Extract embeddings from crawled JSON files and store in Chroma DB."""
    for fname in os.listdir(CRAWL_OUTPUT_DIR):
        if fname.endswith('.json'):
            with open(os.path.join(CRAWL_OUTPUT_DIR, fname), 'r', encoding='utf-8') as f:
                data = json.load(f)
            doc_id = fname.replace('.json', '')
            text = data.get('text', '')
            if not text:
                continue
            embedding = embedder.encode([text])[0].tolist()
            collection.add(
                documents=[text],
                embeddings=[embedding],
                ids=[doc_id]
            )
            print(f"Stored embedding for {doc_id}")

def query_context(query, n_results=2):
    """Query Chroma DB for relevant context."""
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    docs = results.get('documents', [[]])[0]
    return "\n".join(docs)

def call_ollama_with_context(context, query, model=None, host=None):
    """Call Ollama model via HTTP API with the retrieved context and query."""
    if model is None:
        model = OLLAMA_MODEL
    if host is None:
        host = OLLAMA_HOST
    prompt = f"""
Use the context to answer the question.

Context:
{context}

Question: {query}
"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(f"{host}/api/generate", json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except requests.RequestException as e:
        print(f"[ERROR] Could not connect to Ollama at {host}. Is Ollama running and accessible?\nError: {e}")
        sys.exit(1)

def main():
    # Step 1: Crawl all top sites (in parallel, respecting thread limits)
    threads = []
    for url in TOP_SITES:
        t = Thread(target=crawl_and_store, args=(url,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    # Step 2: Extract and store embeddings
    extract_and_store_embeddings()
    # Step 3: Query example
    query = "Latest music news"
    print(f"\nQuery: {query}")
    context = query_context(query)
    print(f"Relevant context:\n{context[:500]}...")
    # Step 4: Call Ollama with context
    print("\nCalling Ollama for LLM answer...")
    answer = call_ollama_with_context(context, query)
    print(f"\nOllama LLM answer:\n{answer}")

if __name__ == "__main__":
    main() 