from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Iterable

from playwright.sync_api import sync_playwright, Page, Response


URL = "https://poeladder.com/ancient"
OUT_FILE = Path("data/ancient_belts.json")

WAIT_MS = 600


def walk(obj: Any) -> Iterable[Any]:
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def looks_like_unique_row(d: dict[str, Any]) -> bool:
    if not d.get("name"):
        return False
    odds_keys = {"tier", "chance", "avgOrbs", "avg_orbs", "minIlvl", "min_ilvl"}
    return any(k in d for k in odds_keys)


def extract_unique_rows(payload: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for node in walk(payload):
        if isinstance(node, dict) and looks_like_unique_row(node):
            out.append(node)
    return out


def norm_name(s: str) -> str:
    return " ".join((s or "").strip().split())


def to_float(x: Any) -> float | None:
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def to_int(x: Any) -> int | None:
    if x is None or x == "":
        return None
    try:
        return int(float(x))
    except Exception:
        return None


def click_category_belt(page: Page) -> None:
    """
    Custom ARIA combobox: find the combobox in the same row as the 'Category:' label,
    open it, then pick 'Belt'.
    """
    # Find the "Category:" label, then look for a combobox near it
    label = page.get_by_text("Category:", exact=False).first
    label.scroll_into_view_if_needed()

    # Heuristic: combobox in the same parent row/container as the label
    row = label.locator("..")
    combo = row.get_by_role("combobox").first

    # If that didn't find it, fall back to any combobox on the page
    if combo.count() == 0:
        combo = page.get_by_role("combobox").first

    combo.scroll_into_view_if_needed()
    combo.click(timeout=20_000)

    # Try the clean ARIA way first: role=option
    opt = page.get_by_role("option", name="Belt", exact=True)
    if opt.count() > 0:
        opt.first.click(timeout=20_000)
    else:
        # Fallback: click by text in the opened list
        page.locator('text="Belt"').first.click(timeout=20_000)

    page.wait_for_timeout(WAIT_MS)


def wait_for_base_dropdown_ready(page: Page) -> None:
    """
    After selecting category, the UI should render a base selector.
    We don't know its exact placeholder text, so we just wait for the API that lists bases.
    """
    # If the page makes an API call listing ancientable bases for that category, great.
    # Otherwise, we fall back to waiting a bit.
    page.wait_for_timeout(1200)

def click_next_page(page: Page) -> bool:
    """
    Click the MUI pagination 'next' IconButton that contains the chevron-right svg path.
    Returns False if it looks disabled / not found.
    """
    # This targets the exact <path> for the chevron-right icon you pasted.
    btn = page.locator('button:has(svg path[d="M8.59 16.34l4.58-4.59-4.58-4.59L10 5.75l6 6-6 6z"])').first

    if btn.count() == 0:
        return False

    # MUI disables pagination buttons with disabled attribute
    if btn.is_disabled():
        return False

    btn.click()
    return True

def first_row_name(page: Page) -> str:
    container = page.locator(".MuiTableContainer-root").first
    rows = container.locator("tbody tr")
    if rows.count() == 0:
        return ""
    cells = rows.nth(0).locator("td")
    if cells.count() < 2:
        return ""
    return (cells.nth(1).inner_text() or "").strip()


def get_open_menu_options(page: Page) -> list[str]:
    """
    Read options ONLY from the currently-open combobox listbox.
    This avoids grabbing random page text.
    """
    # Wait for listbox to appear
    listboxes = page.get_by_role("listbox")
    if listboxes.count() == 0:
        # Some UIs don't use role=listbox; try common menu containers
        # but still avoid scanning the entire page
        menu = page.locator('[role="menu"], [data-radix-popper-content-wrapper], .menu, .dropdown-menu').first
        if menu.count() == 0:
            return []
        texts = menu.locator('div,li,[role="option"],button').all_text_contents()
        return [t.strip() for t in texts if t and t.strip()]

    lb = listboxes.first
    opts = lb.get_by_role("option")
    if opts.count() == 0:
        # Sometimes options are plain elements inside listbox
        texts = lb.locator("div,li,button,[role='option']").all_text_contents()
        return [t.strip() for t in texts if t and t.strip()]

    return [t.strip() for t in opts.all_text_contents() if t and t.strip()]

def extract_belt_table(page: Page):
    container = page.locator(".MuiTableContainer-root").first
    container.wait_for(state="visible", timeout=20_000)

    rows = container.locator("tbody tr")
    count = rows.count()
    print(f"Found {count} belt unique rows.")

    data = []

    for i in range(count):
        row = rows.nth(i)
        cells = row.locator("td")

        if cells.count() < 6:
            continue

        name = cells.nth(1).inner_text().strip()
        tier = cells.nth(2).inner_text().strip()
        min_ilvl = cells.nth(3).inner_text().strip()
        avg_orbs = cells.nth(4).inner_text().strip()
        chance = cells.nth(5).inner_text().strip()

        data.append({
            "name": name,
            "pool": "belt",
            "tier": tier,
            "min_ilvl": int(min_ilvl) if min_ilvl.isdigit() else None,
            "avg_orbs": int(avg_orbs.replace(",", "")) if avg_orbs else None,
            "chance": float(chance.replace("%", "")) / 100 if "%" in chance else None,
            "source": "poeladder (community; Prohibited Library-based)"
        })

    return data



def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # keep visible to reduce bot-blocking
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(2000)

        # 1) Choose category: Belt (combobox-based)
        click_category_belt(page)

        # 2) Wait for the MUI table to render
        page.locator(".MuiTableContainer-root").first.wait_for(state="visible", timeout=20_000)
        page.wait_for_timeout(800)

        # 3) Extract belt outcomes directly from the table
        belt_data = extract_belt_table(page)

        all_rows: dict[str, dict[str, Any]] = {}

        # Read pages until Next is disabled
        while True:
            page_rows = extract_belt_table(page)
            for r in page_rows:
                all_rows[r["name"].lower()] = r  # dedupe by name

            before = first_row_name(page)

            moved = click_next_page(page)
            if not moved:
                break

            # wait for page contents to change
            page.wait_for_timeout(200)
            page.wait_for_function(
                """(prev) => {
                    const first = document.querySelector('.MuiTableContainer-root tbody tr td:nth-child(2)');
                    return first && first.textContent && first.textContent.trim() !== prev;
                }""",
                arg=before,
                timeout=20_000,
            )
            page.wait_for_timeout(300)

        belt_data = sorted(all_rows.values(), key=lambda r: r["name"].lower())


        browser.close()

    # 4) Write snapshot JSON to disk
    OUT_FILE.write_text(
        json.dumps(belt_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(belt_data)} belt rows -> {OUT_FILE}")
    print("Sample:")
    for r in belt_data[:10]:
        print(" -", r["name"], r.get("tier"), r.get("avg_orbs"), r.get("chance"), r.get("min_ilvl"))


if __name__ == "__main__":
    main()
