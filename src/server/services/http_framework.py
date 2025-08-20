import httpx
import asyncio
from typing import Dict, Any, Optional, Set, List
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from .base import AbstractHTTPFramework
from core.logging import logger

class HTTPTestingFramework(AbstractHTTPFramework):
    """Provides functionalities for HTTP request interception and website spidering."""

    async def intercept_request(self, url: str, method: str = 'GET', data: Optional[Dict] = None, headers: Optional[Dict] = None, cookies: Optional[Dict] = None) -> Dict[str, Any]:
        """Sends a custom HTTP request and returns detailed response information."""
        logger.info(f"Intercepting request to {url} with method {method}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, json=data, headers=headers, cookies=cookies, timeout=15)
                response_data = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "cookies": dict(response.cookies),
                    "content": response.text,
                }
                logger.info(f"Request to {url} completed with status {response.status_code}")
                return response_data
            except httpx.RequestError as e:
                logger.error(f"HTTP request to {url} failed: {e}")
                return {"error": str(e)}

    async def spider_website(self, base_url: str, max_depth: int = 2, max_pages: int = 50) -> Dict[str, Any]:
        """Spiders a website to discover pages and links."""
        logger.info(f"Starting spider for {base_url} (max_depth: {max_depth}, max_pages: {max_pages})")
        visited: Set[str] = set()
        to_visit: asyncio.Queue = asyncio.Queue()
        await to_visit.put((base_url, 0))
        found_links: Set[str] = set()

        while not to_visit.empty() and len(visited) < max_pages:
            current_url, depth = await to_visit.get()
            if current_url in visited or depth > max_depth:
                continue

            visited.add(current_url)
            logger.info(f"Spidering: {current_url} at depth {depth}")

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(current_url, follow_redirects=True, timeout=10)
                
                if "text/html" in response.headers.get("content-type", ""):
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        absolute_url = urljoin(current_url, href)
                        if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                            found_links.add(absolute_url)
                            if absolute_url not in visited:
                                await to_visit.put((absolute_url, depth + 1))

            except Exception as e:
                logger.warning(f"Failed to process {current_url}: {e}")

        logger.info(f"Spider finished. Found {len(found_links)} links on {len(visited)} pages.")
        return {"base_url": base_url, "pages_visited": list(visited), "links_found": list(found_links)}

http_testing_framework = HTTPTestingFramework()
