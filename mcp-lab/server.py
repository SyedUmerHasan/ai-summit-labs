import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from markdownify import markdownify
from mcp.server.fastmcp import FastMCP

ZEUS_DIR = Path.home() / ".zeus"
ZEUS_FILE = ZEUS_DIR / "crawler_state.json"

mcp = FastMCP("mcp-lab")


def normalize(url: str) -> str:
    return url.rstrip("/").split("#")[0]


def load_state() -> dict:
    ZEUS_DIR.mkdir(exist_ok=True)
    if ZEUS_FILE.exists():
        raw = json.loads(ZEUS_FILE.read_text())
        return {"visited": set(raw["visited"]), "pending": list(dict.fromkeys(raw["pending"]))}
    return {"visited": set(), "pending": []}


def save_state(state: dict):
    ZEUS_FILE.write_text(json.dumps({"visited": list(state["visited"]), "pending": state["pending"]}, indent=2))


def extract_same_domain_urls(html: str, base_url: str) -> list[str]:
    base_domain = urlparse(base_url).netloc
    soup = BeautifulSoup(html, "html.parser")
    urls = set()
    for tag in soup.find_all("a", href=True):
        full_url = normalize(urljoin(base_url, tag["href"]))
        parsed = urlparse(full_url)
        if parsed.netloc == base_domain and parsed.scheme in ("http", "https"):
            urls.add(full_url)
    return list(urls)


@mcp.tool()
def crawl_url(url: str) -> str:
    """Fetch a URL, save it as markdown under ~/.zeus/crawled/<domain>/, and queue all same-domain links."""
    url = normalize(url)
    state = load_state()

    if url in state["visited"]:
        return f"Already visited: {url}"

    response = httpx.get(url, follow_redirects=True, timeout=15)
    response.raise_for_status()

    html = response.text
    markdown = markdownify(html, heading_style="ATX", strip=["script", "style"])
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    # Save under ~/.zeus/crawled/<domain>/<path>.md
    parsed = urlparse(url)
    out_dir = ZEUS_DIR / "crawled" / parsed.netloc
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^\w\-/]", "_", parsed.path.strip("/")) or "index"
    out_file = out_dir / f"{slug}.md"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(markdown)

    # Update state
    state["visited"].add(url)
    new_urls = extract_same_domain_urls(html, url)
    added = []
    for u in new_urls:
        if u not in state["visited"] and u not in state["pending"]:
            state["pending"].append(u)
            added.append(u)

    save_state(state)

    return (
        f"Saved: {out_file}\n"
        f"Found {len(added)} new same-domain URLs queued.\n"
        f"Total pending: {len(state['pending'])}"
    )


def score_url(url: str, keywords: list[str]) -> int:
    """Score a URL by how many query keywords appear in its path."""
    path = urlparse(url).path.lower()
    return sum(kw in path for kw in keywords)


@mcp.tool()
def recommend_pages(query: str, base_url: str = "") -> dict:
    """
    Given a topic/query, score all known URLs by relevance and return top recommendations.
    Optionally crawl base_url first to seed the URL pool.
    """
    if base_url:
        base_url = normalize(base_url)
        state = load_state()
        if base_url not in state["visited"]:
            crawl_url(base_url)

    state = load_state()
    all_urls = list(state["visited"]) + state["pending"]

    if not all_urls:
        return {"message": "No URLs known yet. Provide a base_url to seed the crawler.", "recommendations": []}

    keywords = re.findall(r"\w+", query.lower())
    scored = sorted(
        ((score_url(u, keywords), u) for u in all_urls),
        key=lambda x: x[0],
        reverse=True,
    )

    top = [{"url": u, "score": s} for s, u in scored if s > 0][:10]
    if not top:
        top = [{"url": u, "score": 0} for _, u in scored[:10]]

    return {
        "query": query,
        "recommendations": top,
        "tip": "Call crawl_url on any of these to fetch and save the page.",
    }



    """Crawl the next pending URL from the queue."""
    state = load_state()
    if not state["pending"]:
        return "No pending URLs."
    next_url = state["pending"].pop(0)
    save_state(state)
    return crawl_url(next_url)


@mcp.tool()
def get_state() -> dict:
    """Return current crawler state (visited + pending URLs)."""
    return load_state()


@mcp.tool()
def clear_state() -> str:
    """Reset the crawler state."""
    save_state({"visited": [], "pending": []})
    return "State cleared."


def main():
    mcp.run()


if __name__ == "__main__":
    main()
