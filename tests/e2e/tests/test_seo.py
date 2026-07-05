"""SEO surface tests: sitemap, robots, canonical, meta, OG tags."""
from __future__ import annotations

import re
import urllib.request
from fixtures import BASE_URL, shot


async def sitemap_xml(page):
    await page.goto(f"{BASE_URL}/sitemap.xml", wait_until="domcontentloaded")
    await shot(page, "30_sitemap")
    body = await page.content()
    assert "<urlset" in body and "/courses" in body, "sitemap missing entries"
    return "sitemap ok"


async def robots_txt(page):
    req = urllib.request.Request(f"{BASE_URL}/robots.txt")
    with urllib.request.urlopen(req, timeout=8) as r:
        body = r.read().decode("utf-8", "ignore")
    assert "User-agent" in body, "robots.txt malformed"
    return f"{len(body)} bytes"


async def landing_meta(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    title = await page.title()
    desc = await page.locator("meta[name='description']").first.get_attribute("content")
    assert title and len(title) > 10, "title too short"
    assert desc and len(desc) > 30, "description too short"
    return f"title={title[:40]!r}"


async def landing_og_tags(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    og_title = await page.locator("meta[property='og:title']").first.get_attribute("content")
    og_type = await page.locator("meta[property='og:type']").first.get_attribute("content")
    assert og_title, "og:title missing"
    assert og_type == "website", f"og:type={og_type}"
    return "og ok"


async def canonical_link(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    href = await page.locator("link[rel='canonical']").first.get_attribute("href")
    assert href and href.startswith("http"), f"bad canonical {href}"
    return href


async def auth_page_noindex(page):
    await page.goto(f"{BASE_URL}/auth", wait_until="domcontentloaded")
    robots = await page.locator("meta[name='robots']").first.get_attribute("content")
    assert robots and "noindex" in robots, f"auth should be noindex, got {robots}"
    return "noindex ok"


async def courses_page_title_unique(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    t1 = await page.title()
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    t2 = await page.title()
    assert t1 != t2, "courses page reuses landing title"
    return f"{t1[:20]!r} vs {t2[:20]!r}"


TESTS = [
    ("seo.sitemap_xml", sitemap_xml),
    ("seo.robots_txt", robots_txt),
    ("seo.landing_meta", landing_meta),
    ("seo.landing_og_tags", landing_og_tags),
    ("seo.canonical_link", canonical_link),
    ("seo.auth_noindex", auth_page_noindex),
    ("seo.unique_titles", courses_page_title_unique),
]
