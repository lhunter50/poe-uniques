from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright


URL = "https://poeladder.com/ancient"


def looks_relevant(url: str) -> bool:
    u = url.lower()
    # keep this broad: we'll capture JSON and sort it out after
    return any(k in u for k in ["ancient", "mythic", "calculator", "api", "data", "weights", "outcomes"])


def safe_name(url: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9._-]+", "_", url)
    return name[:160]


def main() -> None:
    out_dir = Path("ancient_dump")
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        def on_response(resp) -> None:
            try:
                ct = (resp.headers.get("content-type") or "").lower()
                if "application/json" not in ct:
                    return

                rurl = resp.url
                # Capture all JSON, but prefer likely relevant ones
                if not looks_relevant(rurl):
                    # still keep some: many SPAs load JSON from generic endpoints
                    pass

                data: Any = resp.json()
                raw = json.dumps(data, ensure_ascii=False)
                # Skip tiny JSON (often feature flags)
                if len(raw) < 2000:
                    return

                fname = safe_name(rurl) + ".json"
                path = out_dir / fname

                # If duplicates, append counter
                i = 2
                while path.exists():
                    path = out_dir / (safe_name(rurl) + f"__{i}.json")
                    i += 1

                path.write_text(raw, encoding="utf-8")
                saved.append((len(raw), str(path), rurl))
            except Exception:
                return

        page.on("response", on_response)

        page.goto(URL, wait_until="domcontentloaded", timeout=60_000)
        # Let XHRs finish
        page.wait_for_timeout(8_000)

        # Some sites lazy-load on interaction; do a small scroll
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(4_000)

        browser.close()

    saved.sort(reverse=True, key=lambda x: x[0])
    print(f"Saved {len(saved)} JSON files to {out_dir.resolve()}")
    print("Largest files:")
    for size, path, rurl in saved[:10]:
        print(f"- {size:>8} bytes  {path}  <- {rurl}")


if __name__ == "__main__":
    main()
