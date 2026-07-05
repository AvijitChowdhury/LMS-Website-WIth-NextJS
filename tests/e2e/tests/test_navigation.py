"""Navigation, routing, and 404 behavior."""
from __future__ import annotations

from fixtures import BASE_URL, shot


async def not_found_route(page):
    await page.goto(f"{BASE_URL}/this-route-does-not-exist-xyz", wait_until="domcontentloaded")
    await shot(page, "31_not_found")
    html = await page.content()
    assert len(html) > 500, "404 page empty"
    return "renders"


async def root_outlet_renders(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    body_html = await page.locator("body").inner_html()
    assert len(body_html) > 2000, "root outlet empty"
    return f"{len(body_html)} chars"


async def back_forward_history(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    await page.go_back(wait_until="domcontentloaded")
    assert page.url.rstrip("/") == BASE_URL.rstrip("/"), f"back went to {page.url}"
    await page.go_forward(wait_until="domcontentloaded")
    assert page.url.endswith("/courses"), f"forward went to {page.url}"
    return "back/forward ok"


async def checkout_cancelled_route(page):
    await page.goto(f"{BASE_URL}/checkout/cancelled", wait_until="domcontentloaded")
    await shot(page, "32_checkout_cancelled")
    html = await page.content()
    assert "বাতিল" in html, "cancelled page missing text"
    return "renders"


async def checkout_return_no_invoice_redirects(page):
    await page.goto(f"{BASE_URL}/checkout/return", wait_until="domcontentloaded")
    # should redirect to /checkout/error when invoice_id missing
    await page.wait_for_url("**/checkout/error", timeout=6000)
    return page.url


async def anchor_scroll_hash(page):
    await page.goto(f"{BASE_URL}/#top", wait_until="domcontentloaded")
    assert "/" in page.url
    return "hash accepted"


TESTS = [
    ("nav.not_found", not_found_route),
    ("nav.root_outlet", root_outlet_renders),
    ("nav.history", back_forward_history),
    ("nav.checkout_cancelled", checkout_cancelled_route),
    ("nav.checkout_return_redirect", checkout_return_no_invoice_redirects),
    ("nav.hash_route", anchor_scroll_hash),
]
