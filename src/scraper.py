from typing import Optional
from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup


async def fetch_url_async(url: str, timeout: int = 30) -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                return await resp.text()
        except Exception:
            return None


async def extract_links_async(url: str) -> list[dict[str, str]]:
    html = await fetch_url_async(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    links: list[dict[str, str]] = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        full = urljoin(url, href)
        parsed = urlparse(full)
        links.append({
            "url": full,
            "text": tag.get_text(strip=True)[:100],
            "domain": parsed.netloc,
        })
    return links


async def extract_images_async(url: str) -> list[dict[str, str]]:
    html = await fetch_url_async(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    images: list[dict[str, str]] = []
    for tag in soup.find_all("img", src=True):
        src = tag["src"]
        images.append({
            "src": urljoin(url, src),
            "alt": tag.get("alt", ""),
        })
    return images


async def extract_text_async(url: str) -> Optional[str]:
    html = await fetch_url_async(url)
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


async def scrape_with_playwright(url: str) -> Optional[str]:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise ImportError("playwright nao instalado. pip install playwright && playwright install chromium")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            content = await page.content()
            return content
        except Exception:
            return None
        finally:
            await browser.close()
