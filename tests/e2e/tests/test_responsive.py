"""Responsive/viewport smoke checks."""
from __future__ import annotations

from fixtures import BASE_URL, shot


async def mobile_landing(page):
    await page.set_viewport_size({"width": 390, "height": 844})
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    await shot(page, "36_mobile_landing")
    scroll_w = await page.evaluate("document.documentElement.scrollWidth")
    client_w = await page.evaluate("document.documentElement.clientWidth")
    assert scroll_w <= client_w + 2, f"horizontal scroll on mobile: {scroll_w}>{client_w}"
    # restore
    await page.set_viewport_size({"width": 1280, "height": 1800})
    return f"{scroll_w}<={client_w}"


async def tablet_courses(page):
    await page.set_viewport_size({"width": 820, "height": 1180})
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    await shot(page, "37_tablet_courses")
    scroll_w = await page.evaluate("document.documentElement.scrollWidth")
    client_w = await page.evaluate("document.documentElement.clientWidth")
    await page.set_viewport_size({"width": 1280, "height": 1800})
    assert scroll_w <= client_w + 2, f"horizontal scroll on tablet"
    return "no overflow"


async def desktop_landing_hero(page):
    await page.set_viewport_size({"width": 1440, "height": 900})
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    await shot(page, "38_desktop_landing")
    h1 = await page.locator("h1").first.inner_text()
    await page.set_viewport_size({"width": 1280, "height": 1800})
    assert len(h1) > 3, "empty h1 on desktop"
    return f"h1={h1[:40]!r}"


TESTS = [
    ("responsive.mobile_landing", mobile_landing),
    ("responsive.tablet_courses", tablet_courses),
    ("responsive.desktop_landing", desktop_landing_hero),
]
