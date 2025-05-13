# Music Freshness CAG

A Content-Aware Gatherer (CAG) for music freshness, following the workflow in `AiDocs/how_to_create_music_freshness_cag.txt`.

## Features
- Crawls top music news sites with a pool of 6 Python threads (efficient parallel crawling)
- Thread limiting per domain using etcd
- Uses the PageCrawler module to fetch and parse web pages
- Extracts embeddings from crawled content using sentence-transformers
- Stores embeddings in a local Chroma vector database
- Provides a query interface to retrieve relevant context
- Summarizes results using Ollama LLM via HTTP API
- Robust error handling for etcd and Ollama connectivity
- Designed for Docker compatibility

## Requirements
- Python 3.7+
- etcd server (for thread limiting)
- Ollama server (for LLM summarization)
- See `requirements.txt` for Python dependencies

## Environment Variables
- `ETCD_HOST` (default: `localhost`): etcd server host
- `ETCD_PORT` (default: `2379`): etcd server port
- `OLLAMA_HOST` (default: `http://localhost:11434`): Ollama server URL
- `OLLAMA_MODEL` (default: `gemma3:4b`): Ollama model to use

## Usage

### Local
```bash
python fresh/music_freshness_cag.py
```

### Docker
Build the Docker image:
```bash
docker build -t music-freshness-cag -f fresh/Dockerfile .
```

Run the container (ensure etcd and Ollama are accessible):
```bash
docker run --rm --network=host \
  -e ETCD_HOST=localhost \
  -e OLLAMA_HOST=http://localhost:11434 \
  -e OLLAMA_MODEL=gemma3:4b \
  music-freshness-cag
```

If not using `--network=host`, set `ETCD_HOST` and `OLLAMA_HOST` to your host's IP address.

## Workflow
1. Crawls the top music news sites in parallel using a pool of 6 threads, respecting a thread limit per domain using etcd.
2. Uses the PageCrawler to fetch and parse each site, saving output as JSON.
3. Extracts embeddings from the crawled content using sentence-transformers.
4. Stores embeddings in a local Chroma vector database.
5. Provides a query interface to retrieve relevant context for a sample query.
6. Sends the context to Ollama via HTTP API for LLM summarization.
7. Prints the LLM's answer.

## Error Handling
- If etcd is not running or not accessible, the script prints a clear error and exits.
- If Ollama is not running or not accessible, the script prints a clear error and exits.

## Testing
- The program prints crawl and embedding status, and shows a sample query result with an LLM-generated summary.
- You can modify the query in `music_freshness_cag.py` to test different questions.

## Notes
- Make sure both etcd and Ollama servers are running and accessible to the container or local process.
- Chroma DB is used in local mode (no server required).

## License
MIT 