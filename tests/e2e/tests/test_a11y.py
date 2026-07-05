"""Basic accessibility smoke checks."""
from __future__ import annotations

from fixtures import BASE_URL


async def single_h1_on_landing(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    n = await page.locator("h1").count()
    assert n >= 1, "no h1 on landing"
    return f"{n} h1(s)"


async def images_have_alt(page):
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    await page.wait_for_load_state("networkidle", timeout=8000)
    missing = await page.eval_on_selector_all(
        "img",
        "els => els.filter(e => !e.hasAttribute('alt')).length",
    )
    assert missing == 0, f"{missing} img without alt"
    return "all images have alt"


async def buttons_have_names(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    unnamed = await page.eval_on_selector_all(
        "button",
        "els => els.filter(e => !(e.textContent||'').trim() && !e.getAttribute('aria-label') && !e.getAttribute('title')).length",
    )
    assert unnamed < 3, f"{unnamed} buttons without accessible name"
    return f"{unnamed} unnamed buttons"


async def html_lang_set(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    lang = await page.locator("html").first.get_attribute("lang")
    assert lang, "html[lang] missing"
    return f"lang={lang}"


async def viewport_meta(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    content = await page.locator("meta[name='viewport']").first.get_attribute("content")
    assert content and "width=device-width" in content, f"bad viewport {content}"
    return content


async def focusable_skip_link_or_nav(page):
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    # Verify keyboard navigation lands on interactive element
    await page.keyboard.press("Tab")
    tag = await page.evaluate("document.activeElement?.tagName || ''")
    assert tag in ("A", "BUTTON", "INPUT", "SELECT", "TEXTAREA"), f"tab focused {tag}"
    return f"tab→{tag}"


TESTS = [
    ("a11y.single_h1", single_h1_on_landing),
    ("a11y.img_alt", images_have_alt),
    ("a11y.button_names", buttons_have_names),
    ("a11y.html_lang", html_lang_set),
    ("a11y.viewport_meta", viewport_meta),
    ("a11y.keyboard_focus", focusable_skip_link_or_nav),
]
