"""Bengali content + locale formatting checks."""
from __future__ import annotations

from fixtures import BASE_URL


BENGALI_RANGE = ("\u0980", "\u09ff")


def _has_bengali(s: str) -> bool:
    return any(BENGALI_RANGE[0] <= c <= BENGALI_RANGE[1] for c in s)


async def landing_has_bengali(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    text = await page.locator("body").inner_text()
    assert _has_bengali(text), "no bengali on landing"
    return "bn ok"


async def courses_has_bengali(page):
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    text = await page.locator("body").inner_text()
    assert _has_bengali(text), "no bengali on courses"
    return "bn ok"


async def bdt_symbol_present(page):
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    text = await page.locator("body").inner_text()
    # Either ৳ or Bengali digits or the word টাকা
    assert "৳" in text or "টাকা" in text or any(d in text for d in "০১২৩৪৫৬৭৮৯"), "no BDT/bengali numerals"
    return "currency ok"


async def auth_page_has_bengali_labels(page):
    await page.goto(f"{BASE_URL}/auth", wait_until="domcontentloaded")
    text = await page.locator("body").inner_text()
    assert _has_bengali(text), "auth page not localized"
    return "auth localized"


TESTS = [
    ("i18n.landing_bn", landing_has_bengali),
    ("i18n.courses_bn", courses_has_bengali),
    ("i18n.currency", bdt_symbol_present),
    ("i18n.auth_bn", auth_page_has_bengali_labels),
]
