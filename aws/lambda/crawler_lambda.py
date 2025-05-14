import os
import json
import logging
import etcd3
import chromadb
from sentence_transformers import SentenceTransformer
from urllib.parse import urlparse
import importlib.util
import pathlib
import time

# Configuration from environment
TOP_SITES = [
    "https://www.billboard.com/",
    "https://pitchfork.com/",
    "https://www.rollingstone.com/",
    "https://www.nme.com/"
]
THREAD_LIMIT = 5
ETCD_HOST = os.environ.get("ETCD_HOST", "localhost")
ETCD_PORT = int(os.environ.get("ETCD_PORT", 2379))
CRAWL_OUTPUT_DIR = "/tmp/crawled_json"  # Use /tmp for Lambda
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_COLLECTION = "music_freshness"

# Lambda: initialize heavy resources outside handler for cold start efficiency
os.makedirs(CRAWL_OUTPUT_DIR, exist_ok=True)

def safe_etcd_client(host, port):
    try:
        client = etcd3.client(host=host, port=port)
        # Test connection by putting and getting a test key
        test_key = "cag_etcd_test_key"
        client.put(test_key, "test")
        value, _ = client.get(test_key)
        client.delete(test_key)
        if value != b"test":
            raise Exception("etcd test key mismatch")
        return client
    except Exception as e:
        logging.error(f"[ERROR] Could not connect to etcd at {host}:{port}: {e}")
        raise

etcd = safe_etcd_client(ETCD_HOST, ETCD_PORT)
embedder = SentenceTransformer(EMBEDDING_MODEL)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)

utils_path = pathlib.Path(__file__).parent.parent.parent / 'utils' / 'page_crawler.py'
spec = importlib.util.spec_from_file_location('page_crawler', str(utils_path))
page_crawler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(page_crawler)
PageCrawler = page_crawler.PageCrawler
crawler = PageCrawler()

def get_domain(url):
    return urlparse(url).netloc.replace('www.', '')

def acquire_thread_slot(domain):
    prefix = f"/crawler/semaphores/{domain}/"
    keys = list(etcd.get_prefix(prefix, keys_only=True))
    if len(keys) < THREAD_LIMIT:
        lease = etcd.lease(300)
        thread_id = str(os.urandom(8).hex())
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
            time.sleep(2)
        # Crawl and save
        output_file = os.path.join(CRAWL_OUTPUT_DIR, f"{domain}.json")
        crawler.crawl_and_save(url, output_file)
        return output_file, None
    except Exception as e:
        return None, str(e)
    finally:
        release_thread_slot(key, lease)

def extract_and_store_embeddings():
    results = []
    for fname in os.listdir(CRAWL_OUTPUT_DIR):
        if fname.endswith('.json'):
            try:
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
                results.append((doc_id, None))
            except Exception as e:
                results.append((fname, str(e)))
    return results

def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    crawl_results = []
    for url in TOP_SITES:
        output_file, error = crawl_and_store(url)
        crawl_results.append({"url": url, "output_file": output_file, "error": error})
    embed_results = extract_and_store_embeddings()
    errors = [r for r in crawl_results if r["error"]] + [r for r in embed_results if r[1]]
    return {
        "statusCode": 200 if not errors else 500,
        "body": json.dumps({
            "crawled": crawl_results,
            "embeddings": embed_results,
            "errors": errors,
            "message": "Crawler Lambda completed" if not errors else "Crawler Lambda completed with errors"
        })
    } 