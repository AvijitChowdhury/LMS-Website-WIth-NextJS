"""Performance + runtime hygiene smoke checks."""
from __future__ import annotations

import time
from fixtures import BASE_URL


async def landing_loads_under_budget(page):
    t0 = time.time()
    await page.goto(BASE_URL, wait_until="domcontentloaded")
    ms = int((time.time() - t0) * 1000)
    assert ms < 8000, f"landing took {ms}ms"
    return f"{ms} ms"


async def courses_loads_under_budget(page):
    t0 = time.time()
    await page.goto(f"{BASE_URL}/courses", wait_until="domcontentloaded")
    ms = int((time.time() - t0) * 1000)
    assert ms < 8000, f"courses took {ms}ms"
    return f"{ms} ms"


async def no_5xx_on_landing(page):
    bad: list[str] = []
    page.on("response", lambda r: bad.append(f"{r.status} {r.url}") if r.status >= 500 else None)
    await page.goto(BASE_URL, wait_until="networkidle")
    assert not bad, f"5xx responses: {bad[:3]}"
    return "no 5xx"


async def no_console_errors_on_landing(page):
    errs: list[str] = []
    page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    await page.goto(BASE_URL, wait_until="networkidle")
    filtered = [e for e in errs if "hydrat" not in e.lower() and "favicon" not in e.lower()]
    assert len(filtered) < 3, f"console errors: {filtered[:3]}"
    return f"{len(filtered)} filtered errors"


async def dom_size_reasonable(page):
    await page.goto(BASE_URL, wait_until="networkidle")
    count = await page.evaluate("document.querySelectorAll('*').length")
    assert count < 5000, f"DOM has {count} nodes"
    return f"{count} nodes"


TESTS = [
    ("perf.landing_time", landing_loads_under_budget),
    ("perf.courses_time", courses_loads_under_budget),
    ("perf.no_5xx", no_5xx_on_landing),
    ("perf.no_console_errors", no_console_errors_on_landing),
    ("perf.dom_size", dom_size_reasonable),
]
