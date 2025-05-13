"""
Test program for the PageCrawler utility.

This script uses the PageCrawler to scrape https://www.billboard.com,
saves the output to a JSON file, and prints the results.

Usage:
    python tests/test_page_crawler.py
"""

import sys
import os
import json

# Ensure the project root is in sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.page_crawler import PageCrawler

def test_billboard_crawl():
    url = 'https://www.billboard.com'
    output_file = 'tests/billboard_output.json'
    crawler = PageCrawler()
    print(f"Crawling {url} ...")
    crawler.crawl_and_save(url, output_file)
    assert os.path.exists(output_file), f"Output file {output_file} was not created."
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    assert 'title' in data and data['title'], "Title not found in output."
    assert 'text' in data and data['text'], "Text not found in output."
    print("Crawl successful! Title:")
    print(data['title'])
    print("\nFirst 500 characters of text:")
    print(data['text'][:500])

if __name__ == '__main__':
    test_billboard_crawl() 