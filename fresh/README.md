# Music Freshness CAG

A Content-Aware Gatherer (CAG) for music freshness, following the workflow in `AiDocs/how_to_create_music_freshness_cag.txt`.

## Features
- Crawls top music news sites with thread limiting using etcd
- Uses the PageCrawler module to fetch and parse web pages
- Extracts embeddings from crawled content using sentence-transformers
- Stores embeddings in a local Chroma vector database
- Provides a query interface to retrieve relevant context
- Designed for Docker compatibility

## Requirements
- Python 3.7+
- etcd server (for thread limiting)
- See `requirements.txt` for Python dependencies

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

Run the container (ensure etcd is accessible):
```bash
docker run --rm --network=host -e ETCD_HOST=localhost music-freshness-cag
```

## Workflow
1. Crawls the top music news sites in parallel, respecting a thread limit per domain using etcd.
2. Uses the PageCrawler to fetch and parse each site, saving output as JSON.
3. Extracts embeddings from the crawled content using sentence-transformers.
4. Stores embeddings in a local Chroma vector database.
5. Provides a query interface to retrieve relevant context for a sample query.

## Testing
- The program prints crawl and embedding status, and shows a sample query result.
- You can modify the query in `music_freshness_cag.py` to test different questions.

## Notes
- Make sure an etcd server is running and accessible to the container or local process.
- Chroma DB is used in local mode (no server required).

## License
MIT 