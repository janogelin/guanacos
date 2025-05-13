"""
page_crawler.py

A simple web page crawler that fetches a URL, parses its content using BeautifulSoup,
and stores the extracted data in a JSON file.

Features:
- Fetches HTML content from a given URL
- Parses the page title and all text content
- Stores the results in a JSON file

Dependencies:
- requests
- beautifulsoup4

Usage:
    from utils.page_crawler import PageCrawler
    crawler = PageCrawler()
    crawler.crawl_and_save('https://example.com', 'output.json')

"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, Any

class PageCrawler:
    """
    A simple web page crawler that fetches a URL, parses its content using BeautifulSoup,
    and stores the extracted data in a JSON file.
    """

    def fetch_page(self, url: str) -> str:
        """
        Fetch the HTML content of the given URL.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: The HTML content of the page.

        Raises:
            requests.RequestException: If the request fails.
        Note:
            Some websites may block requests with the default user agent. This method sets a common browser User-Agent header to improve compatibility.
        """
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/122.0.0.0 Safari/537.36'
            )
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def parse_content(self, html: str) -> Dict[str, Any]:
        """
        Parse the HTML content using BeautifulSoup and extract useful information.

        Args:
            html (str): The HTML content to parse.

        Returns:
            Dict[str, Any]: A dictionary containing the page title and all visible text.
        """
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else ''
        # Extract all visible text
        texts = soup.stripped_strings
        visible_text = ' '.join(texts)
        return {
            'title': title,
            'text': visible_text
        }

    def save_to_json(self, data: Dict[str, Any], filename: str) -> None:
        """
        Save the extracted data to a JSON file.

        Args:
            data (Dict[str, Any]): The data to save.
            filename (str): The path to the output JSON file.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def crawl_and_save(self, url: str, output_file: str) -> None:
        """
        Fetch a web page, parse its content, and save the results to a JSON file.

        Args:
            url (str): The URL to crawl.
            output_file (str): The path to the output JSON file.
        """
        html = self.fetch_page(url)
        data = self.parse_content(html)
        self.save_to_json(data, output_file) 