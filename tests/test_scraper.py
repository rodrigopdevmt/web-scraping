import pytest
from src.scraper import extract_links_async, extract_text_async


@pytest.mark.asyncio
async def test_extract_links_async():
    links = await extract_links_async("https://example.com")
    assert isinstance(links, list)


@pytest.mark.asyncio
async def test_extract_text_async():
    text = await extract_text_async("https://example.com")
    assert text is not None
    assert "Example" in text
