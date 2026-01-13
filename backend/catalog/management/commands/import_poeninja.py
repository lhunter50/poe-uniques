from __future__ import annotations

import json
import time
from typing import Any, Final, Iterable, Iterator, NotRequired, TypedDict, cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from catalog.models import (
    BaseItem,
    League,
    UniqueItem,
    UniqueItemLeaguePresence,
)

POE_NINJA_ITEMOVERVIEW_URL: Final[str] = "https://poe.ninja/api/data/itemoverview"

DEFAULT_TYPES: Final[list[str]] = [
    "UniqueArmour",
    "UniqueWeapon",
    "UniqueAccessory",
    "UniqueFlask",
    "UniqueJewel",
    ]


class PoeNinjaLine(TypedDict, total=False):
    # Common fields (vary by type)
    name: str
    baseType: str
    typeLine: str
    icon: str
    levelRequired: int

    explicitMods: list[str]
    implicitMods: list[str]
    flavourText: list[str] | str


class PoeNinjaPayload(TypedDict):
    lines: list[PoeNinjaLine]
    # There are other keys like "currencyDetails" etc depending on endpoint,
    # but we only care about "lines" here.


def fetch_json(url: str, *, timeout_s: int = 30) -> dict[str, Any]:
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
    return cast(dict[str, Any], json.loads(raw))


def coalesce_str(*vals: object) -> str:
    for v in vals:
        if v is None:
            continue
        s = str(v).strip()
        if s:
            return s
    return ""


def to_text(val: object) -> str:
    """
    poe.ninja commonly uses lists for mod lines.
    Convert list[str] -> newline text, str -> stripped.
    """
    if isinstance(val, list):
        return "\n".join(str(x) for x in val if x is not None).strip()
    if isinstance(val, str):
        return val.strip()
    return ""


def iter_lines(payload: dict[str, Any]) -> Iterator[PoeNinjaLine]:
    raw_lines = payload.get("lines", [])
    if isinstance(raw_lines, list):
        for row in raw_lines:
            if isinstance(row, dict):
                # We accept it as PoeNinjaLine-like; missing keys are fine (TypedDict total=False)
                yield cast(PoeNinjaLine, row)


def parse_required_level(val: object) -> int | None:
    if val is None:
        return None
    try:
        n = int(val)
    except (TypeError, ValueError):
        return None
    return n if n >= 0 else None


class Command(BaseCommand):
    help = "Import uniques/base items from poe.ninja itemoverview endpoints."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--league",
            default="Standard",
            help="League name (e.g. Standard, Settlers). Default: Standard",
        )
        parser.add_argument(
            "--types",
            nargs="*",
            default=list(DEFAULT_TYPES),
            help=f"poe.ninja itemoverview types. Default: {', '.join(DEFAULT_TYPES)}",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=0.4,
            help="Seconds to sleep between requests. Default: 0.4",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Fetch/parse but do not write to the DB.",
        )

    def handle(self, *args: object, **opts: object) -> None:
        league_name = str(opts.get("league", "Standard")).strip()
        types = cast(list[str], opts.get("types", list(DEFAULT_TYPES)))
        sleep_s = float(opts.get("sleep", 0.4) or 0.0)
        dry_run = bool(opts.get("dry_run", False))

        if not league_name:
            raise SystemExit("--league cannot be blank")
        if not types:
            raise SystemExit("--types cannot be empty")

        self.stdout.write(self.style.MIGRATE_HEADING(f"Importing league={league_name}, types={types}"))

        league_obj, _ = League.objects.get_or_create(name=league_name)
        now = timezone.now()

        totals: dict[str, int] = {
            "base_created": 0,
            "base_touched": 0,
            "unique_created": 0,
            "unique_updated": 0,
            "presence_upserted": 0,
        }

        for t in types:
            url = f"{POE_NINJA_ITEMOVERVIEW_URL}?{urlencode({'league': league_name, 'type': t})}"
            self.stdout.write(self.style.HTTP_INFO(f"GET {url}"))

            payload = fetch_json(url)
            rows = list(iter_lines(payload))
            self.stdout.write(self.style.SUCCESS(f"  -> {len(rows)} rows"))

            if dry_run:
                time.sleep(sleep_s)
                continue

            # One atomic block per type keeps DB consistent and performance reasonable
            with transaction.atomic():
                for row in rows:
                    unique_name = coalesce_str(row.get("name"))
                    base_name = coalesce_str(row.get("baseType"), row.get("typeLine"))

                    if not unique_name or not base_name:
                        continue

                    image_url = coalesce_str(row.get("icon"))
                    required_level = parse_required_level(row.get("levelRequired"))

                    implicit = to_text(row.get("implicitMods"))
                    explicit = to_text(row.get("explicitMods"))
                    raw_mods = "\n".join([part for part in (implicit, explicit) if part]).strip()

                    flavour = to_text(row.get("flavourText"))

                    base_obj, base_created = BaseItem.objects.get_or_create(
                        name=base_name,
                        defaults={"item_class": BaseItem.ItemClass.OTHER, "slot": None},
                    )
                    if base_created:
                        totals["base_created"] += 1
                    totals["base_touched"] += 1

                    poe_id = row.get("id")
                    if poe_id is None:
                        continue

                    unique_obj, created = UniqueItem.objects.update_or_create(
                        poe_ninja_id = poe_id,
                        defaults={
                            "name": unique_name,
                            "base_item": base_obj,
                            "required_level": required_level,
                            "image_url": image_url,
                            "raw_mods": raw_mods,
                            "flavour_text": flavour,
                        },
                    )
                    if created:
                        totals["unique_created"] += 1
                    else:
                        totals["unique_updated"] += 1

                    pres_obj, pres_created = UniqueItemLeaguePresence.objects.get_or_create(
                        unique_item=unique_obj,
                        league=league_obj,
                        defaults={"first_seen_at": now, "last_seen_at": now},
                    )
                    if not pres_created:
                        pres_obj.last_seen_at = now
                        pres_obj.save(update_fields=["last_seen_at"])

                    totals["presence_upserted"] += 1

            time.sleep(sleep_s)

        self.stdout.write(self.style.SUCCESS("Done."))
        self.stdout.write(
            "BaseItem: created={base_created} touched={base_touched}\n"
            "UniqueItem: created={unique_created} updated={unique_updated}\n"
            "Presence: upserted={presence_upserted}".format(**totals)
        )
