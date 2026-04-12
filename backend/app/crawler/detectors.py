import re
import json
import os
from typing import Optional

# Pre-compiled signature cache
_SIGNATURES: list[dict] = []
_COMPILED: dict[str, re.Pattern] = {}


def load_signatures() -> list[dict]:
    """Load and pre-compile all detection signatures from signatures.json."""
    global _SIGNATURES, _COMPILED
    if _SIGNATURES:
        return _SIGNATURES

    sig_path = os.path.join(os.path.dirname(__file__), "..", "signatures", "signatures.json")
    with open(sig_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _SIGNATURES = data["technologies"]

    for tech in _SIGNATURES:
        for det in tech.get("detectors", []):
            key = f"{tech['slug']}:{det['pattern']}"
            _COMPILED[key] = re.compile(det["pattern"], re.IGNORECASE)

    return _SIGNATURES


def get_compiled(slug: str, pattern: str) -> re.Pattern:
    key = f"{slug}:{pattern}"
    return _COMPILED[key]


def extract_signals(html: str, headers: dict, soup) -> dict:
    """Extract all signal sources from a fetched page."""
    script_srcs = [s.get("src", "") for s in soup.find_all("script", src=True)]
    meta_tags = {}
    for m in soup.find_all("meta"):
        name = m.get("name", m.get("property", ""))
        content = m.get("content", "")
        if name:
            meta_tags[name] = content

    link_hrefs = [l.get("href", "") for l in soup.find_all("link", href=True)]
    cookies = headers.get("set-cookie", "")

    return {
        "html": html,
        "script_srcs": script_srcs,
        "meta_tags": meta_tags,
        "link_hrefs": link_hrefs,
        "headers": headers,
        "cookies": cookies,
        "title": soup.title.string.strip() if soup.title and soup.title.string else "",
    }


def match_detector(detector: dict, signals: dict, slug: str) -> Optional[str]:
    """Match a single detector against signals. Returns evidence snippet or None."""
    dtype = detector["type"]
    pattern = get_compiled(slug, detector["pattern"])

    if dtype == "html":
        m = pattern.search(signals["html"])
        if m:
            start = max(0, m.start() - 30)
            end = min(len(signals["html"]), m.end() + 30)
            return signals["html"][start:end][:200]

    elif dtype == "script_src":
        for src in signals["script_srcs"]:
            m = pattern.search(src)
            if m:
                return src[:200]

    elif dtype == "meta":
        for name, content in signals["meta_tags"].items():
            combined = f"{name}: {content}"
            m = pattern.search(combined)
            if m:
                return combined[:200]

    elif dtype == "link_href":
        for href in signals["link_hrefs"]:
            m = pattern.search(href)
            if m:
                return href[:200]

    elif dtype == "header":
        # Pattern format can match against all headers
        for hname, hval in signals["headers"].items():
            combined = f"{hname}: {hval}"
            m = pattern.search(combined)
            if m:
                return combined[:200]

    elif dtype == "cookie":
        m = pattern.search(signals["cookies"])
        if m:
            start = max(0, m.start() - 20)
            end = min(len(signals["cookies"]), m.end() + 20)
            return signals["cookies"][start:end][:200]

    return None


def run_detectors(signals: dict) -> list[dict]:
    """Run all signatures against extracted signals. Returns list of detections."""
    signatures = load_signatures()
    detections = []

    for tech in signatures:
        for detector in tech.get("detectors", []):
            evidence = match_detector(detector, signals, tech["slug"])
            if evidence:
                detections.append({
                    "name": tech["name"],
                    "slug": tech["slug"],
                    "category": tech["category"],
                    "website": tech.get("website"),
                    "description": tech.get("description"),
                    "evidence": evidence,
                    "confidence": 1.0,
                })
                break  # one match per tech is enough

    return detections
