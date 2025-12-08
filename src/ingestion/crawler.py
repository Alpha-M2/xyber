"""Document crawler for Xyber documentation."""

import asyncio
from typing import List, Optional, Set
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


class DocumentCrawler:
    """Web crawler for fetching documentation."""

    def __init__(self, base_url: str, max_depth: int = 3):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited: Set[str] = set()
        self.domain = urlparse(base_url).netloc

    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain."""
        parsed = urlparse(url)
        return parsed.netloc == self.domain and url not in self.visited

    async def fetch_page(
        self, session: aiohttp.ClientSession, url: str
    ) -> Optional[str]:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
        except Exception:
            pass
        return None

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all links from HTML."""
        soup = BeautifulSoup(html, "lxml")
        links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            # Convert relative URLs to absolute
            absolute_url = urljoin(base_url, href)
            # Remove fragments
            absolute_url = absolute_url.split("#")[0]

            if self.is_valid_url(absolute_url):
                links.append(absolute_url)

        return links

    def extract_content(self, html: str) -> str:
        """Extract main content from HTML."""
        soup = BeautifulSoup(html, "lxml")

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        text = soup.get_text(separator="\n")

        # Clean up whitespace
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)

    async def crawl_depth(
        self, session: aiohttp.ClientSession, url: str, current_depth: int
    ) -> dict:
        """Recursively crawl with depth tracking."""
        if current_depth > self.max_depth or url in self.visited:
            return {}

        self.visited.add(url)
        # ...existing code...

        html = await self.fetch_page(session, url)
        if not html:
            return {}

        content = self.extract_content(html)
        results = {url: content}

        # Continue crawling child links
        if current_depth < self.max_depth:
            links = self.extract_links(html, url)
            tasks = [
                self.crawl_depth(session, link, current_depth + 1)
                for link in links[:10]  # Limit concurrent requests
            ]

            for task_result in asyncio.as_completed(tasks):
                try:
                    child_results = await task_result
                    results.update(child_results)
                except Exception as e:
                    logger.error(f"Error in crawl_depth: {str(e)}")

        return results

    async def crawl(self) -> dict:
        """Start the crawling process."""
        # ...existing code...

        async with aiohttp.ClientSession() as session:
            results = await self.crawl_depth(session, self.base_url, 0)

        # ...existing code...
        return results


async def crawl_xyber_docs(
    url: str = "https://docs.xyber.inc/", max_depth: int = 5
) -> dict:
    """Convenience function to crawl Xyber docs."""
    crawler = DocumentCrawler(url, max_depth=max_depth)
    return await crawler.crawl()
