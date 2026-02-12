from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}


def get_all_links(url, max_pages=5):
    visited = set()
    to_visit = [url]
    found_links = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=HEADERS, timeout=8)
            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                absolute = urljoin(current_url, link["href"])

                # stay inside same domain
                if urlparse(absolute).netloc == urlparse(url).netloc:
                    if absolute not in visited:
                        to_visit.append(absolute)
                        found_links.append(absolute)

        except requests.exceptions.RequestException:
            pass

    return list(set(found_links))
