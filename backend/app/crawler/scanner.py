from __future__ import annotations

import httpx
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dataclasses import dataclass, field
from typing import Optional

from app.crawler.detectors import extract_signals, run_detectors
from app.crawler.icp import extract_icp

CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


@dataclass
class ScanResult:
    url: str
    domain: str
    title: str = ""
    meta_description: str = ""
    icp_number: Optional[str] = None
    server_header: Optional[str] = None
    status_code: int = 0
    response_time_ms: int = 0
    html_size_bytes: int = 0
    detections: list = field(default_factory=list)
    error: Optional[str] = None


def normalize_url(raw: str) -> str:
    """Accept bare domains like 'taobao.com' and turn into full URL."""
    raw = raw.strip()
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    parsed = urlparse(raw)
    if not parsed.path or parsed.path == "":
        raw = raw + "/"
    return raw


def extract_domain(url: str) -> str:
    """Extract clean domain from URL, stripping www. prefix."""
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split("/")[0]
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


async def scan_url(url: str) -> ScanResult:
    """Fetch a URL and run all detection signatures against it."""
    url = normalize_url(url)
    domain = extract_domain(url)

    result = ScanResult(url=url, domain=domain)

    try:
        start = time.monotonic()
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": CHROME_UA},
        ) as client:
            response = await client.get(url)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        result.status_code = response.status_code
        result.response_time_ms = elapsed_ms
        result.html_size_bytes = len(response.content)
        result.server_header = response.headers.get("server")

        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        if soup.title and soup.title.string:
            result.title = soup.title.string.strip()[:500]

        # Extract meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result.meta_description = meta_desc["content"][:500]

        # Extract ICP
        icp_data = extract_icp(html)
        result.icp_number = icp_data.get("icp_number")

        # Extract signals and run detectors
        headers_dict = {k.lower(): v for k, v in response.headers.items()}
        signals = extract_signals(html, headers_dict, soup)
        result.detections = run_detectors(signals)

    except Exception as e:
        result.error = str(e)[:500]

    return result
