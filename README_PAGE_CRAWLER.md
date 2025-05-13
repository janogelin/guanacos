# Page Crawler Utility

A simple web page crawler implemented in Python using BeautifulSoup and Requests. It fetches a web page, extracts the title and all visible text, and stores the results in a JSON file.

## Features
- Fetches HTML content from a given URL
- Parses the page title and all visible text
- Stores the results in a JSON file

## Requirements
- Python 3.7+
- `requests`
- `beautifulsoup4`

Install dependencies (if not already installed):

```bash
pip install requests beautifulsoup4
```

## Usage

Import and use the crawler in your Python code:

```python
from utils.page_crawler import PageCrawler

crawler = PageCrawler()
crawler.crawl_and_save('https://example.com', 'output.json')
```

This will fetch the page at `https://example.com`, extract the title and all visible text, and save the results to `output.json`.

## Example Output

```json
{
    "title": "Example Domain",
    "text": "Example Domain This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission. More information..."
}
```

## Testing

A test program is provided to demonstrate usage and test the crawler with [https://www.billboard.com](https://www.billboard.com).

To run the test:

```bash
python tests/test_page_crawler.py
```

## License
MIT 