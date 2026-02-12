from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.request import Request, urlopen


DUMP_FILE = Path("ancient_dump/https_poeladder.com_api_v1_uniques_bases_ancientable_1.json")
OUT_FILE = Path("data/ancient_belts.json")

SLEEP_S = 0.25  # be polite


def fetch_json(url: str, *, timeout_s: int = 30) -> Any:
    req = Request(
        url,
        headers={
            "User-Agent": "poe-uniques-importer/1.0 (+django)",
            "Accept": "application/json",
        },
        method="GET",
    )
    with urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def find_belt_bases(payload: Any) -> list[dict[str, Any]]:
    """
    Expected shape:
    { ..., "baseItems": [ { "category": "Amulet", "baseItems": [ ... ] }, ... ] }

    Returns the list of base items under category "Belt".
    """
    if not isinstance(payload, dict):
        raise ValueError("Dump payload is not a dict")

    groups = payload.get("baseItems")
    if not isinstance(groups, list):
        raise ValueError("Dump payload has no 'baseItems' list")

    for g in groups:
        if not isinstance(g, dict):
            continue
        if str(g.get("category", "")).lower() == "belt":
            bases = g.get("baseItems", [])
            if isinstance(bases, list):
                # each item should have: name, identifier, url, uniqueCount
                return [b for b in bases if isinstance(b, dict) and b.get("url")]
    return []


def walk(obj: Any) -> Iterable[Any]:
    """Yield all nested values (dict/list tree walk)."""
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def looks_like_unique_row(d: dict[str, Any]) -> bool:
    # We expect at least a name, and at least one of these odds-ish fields.
    if not d.get("name"):
        return False
    keys = set(d.keys())
    odds_keys = {"tier", "chance", "avgOrbs", "avg_orbs", "minIlvl", "min_ilvl"}
    return len(keys.intersection(odds_keys)) > 0


def extract_unique_rows(any_payload: Any) -> list[dict[str, Any]]:
    """
    We don't know the exact per-base payload shape yet, so we:
    - walk all nested dicts
    - keep dicts that look like unique entries with odds fields
    """
    out: list[dict[str, Any]] = []
    for node in walk(any_payload):
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


def main() -> None:
    if not DUMP_FILE.exists():
        raise SystemExit(f"Missing dump file: {DUMP_FILE}")

    dump = json.loads(DUMP_FILE.read_text(encoding="utf-8"))
    belt_bases = find_belt_bases(dump)
    if not belt_bases:
        raise SystemExit("Could not find category 'Belt' in dump JSON")

    print(f"Found {len(belt_bases)} belt bases")

    all_uniques: dict[str, dict[str, Any]] = {}

    for i, base in enumerate(belt_bases, start=1):
        base_name = base.get("name")
        url = base.get("url")
        if not url:
            continue

        print(f"[{i}/{len(belt_bases)}] {base_name} -> {url}")

        payload = fetch_json(str(url))
        candidates = extract_unique_rows(payload)

        # Convert candidates into our normalized format
        for c in candidates:
            name = norm_name(str(c.get("name", "")))
            if not name:
                continue

            tier = c.get("tier")
            chance = to_float(c.get("chance"))
            avg_orbs = to_int(c.get("avgOrbs") if "avgOrbs" in c else c.get("avg_orbs"))
            min_ilvl = to_int(c.get("minIlvl") if "minIlvl" in c else c.get("min_ilvl"))

            row = {
                "name": name,
                "pool": "belt",
                "tier": tier,
                "chance": chance,       # float 0..100? or 0..1? depends on source; we'll keep raw
                "avg_orbs": avg_orbs,
                "min_ilvl": min_ilvl,
                "source": "poeladder (community; Prohibited Library-based)",
            }

            # Deduplicate by name: keep the row with the *lowest* avg_orbs if present
            key = name.lower()
            existing = all_uniques.get(key)
            if existing is None:
                all_uniques[key] = row
            else:
                old = existing.get("avg_orbs")
                new = row.get("avg_orbs")
                if isinstance(new, int) and (not isinstance(old, int) or new < old):
                    all_uniques[key] = row

        time.sleep(SLEEP_S)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    out_list = sorted(all_uniques.values(), key=lambda r: r["name"].lower())
    OUT_FILE.write_text(json.dumps(out_list, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nWrote {len(out_list)} unique belt rows to: {OUT_FILE}")
    print("Sample:")
    for r in out_list[:10]:
        print(" -", r["name"], r.get("tier"), r.get("avg_orbs"), r.get("chance"), r.get("min_ilvl"))


if __name__ == "__main__":
    main()
