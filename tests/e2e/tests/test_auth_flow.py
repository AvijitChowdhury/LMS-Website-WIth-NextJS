"""Auth surface UI tests (do not sign in — the runner is already signed in)."""
from __future__ import annotations

from fixtures import BASE_URL, shot


async def logged_in_redirects_from_auth(page):
    await page.goto(f"{BASE_URL}/auth", wait_until="domcontentloaded")
    # Already-authenticated users get redirected to /dashboard or /admin
    try:
        await page.wait_for_url("**/dashboard**", timeout=4000)
    except Exception:
        await page.wait_for_url("**/admin**", timeout=4000)
    await shot(page, "33_auth_redirect")
    assert "/auth" not in page.url, f"stuck on /auth: {page.url}"
    return page.url


async def dashboard_profile_page(page):
    await page.goto(f"{BASE_URL}/dashboard/profile", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    await shot(page, "34_profile")
    assert "/auth" not in page.url
    inputs = await page.locator("input").count()
    assert inputs > 0, "no profile inputs"
    return f"{inputs} inputs"


async def dashboard_orders_page(page):
    await page.goto(f"{BASE_URL}/dashboard/orders", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    await shot(page, "35_orders")
    assert "/auth" not in page.url
    html = await page.content()
    assert "অর্ডার" in html
    return "orders reachable"


TESTS = [
    ("auth.redirect_when_signed_in", logged_in_redirects_from_auth),
    ("auth.dashboard_profile", dashboard_profile_page),
    ("auth.dashboard_orders", dashboard_orders_page),
]
