from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import UniqueItem, UniqueAncientMeta


def normalize_name(s: str) -> str:
    return " ".join((s or "").strip().split())


class Command(BaseCommand):
    help = "Import Ancient Orb tier/odds metadata from JSON snapshot."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--file",
            required=True,
            help="Path to JSON file (e.g. data/ancient_belts.json)",
        )
        parser.add_argument(
            "--pool",
            default="belt",
            help="Pool key (default: belt)",
        )

    def handle(self, *args: object, **opts: object) -> None:
        file_path = Path(str(opts["file"])).expanduser().resolve()
        pool = str(opts.get("pool") or "belt").strip().lower()

        if not file_path.exists():
            raise SystemExit(f"File not found: {file_path}")

        raw = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise SystemExit("JSON must be a list of objects")

        # Build lookup map of uniques by normalized name
        uniques = {
            normalize_name(u.name).lower(): u
            for u in UniqueItem.objects.all()
        }

        updated = 0
        missing = []

        with transaction.atomic():
            for row in raw:
                if not isinstance(row, dict):
                    continue

                name = normalize_name(str(row.get("name") or "")).lower()
                if not name:
                    continue

                unique = uniques.get(name)
                if not unique:
                    missing.append(name)
                    continue

                tier_raw = row.get("tier")
                try:
                    tier = int(tier_raw)
                except (TypeError, ValueError):
                    tier = None

                chance = row.get("chance")
                avg_orbs = row.get("avg_orbs")
                min_ilvl = row.get("min_ilvl")
                source = row.get("source")

                UniqueAncientMeta.objects.update_or_create(
                    unique_item=unique,
                    defaults={
                        "pool": pool,
                        "tier": tier,
                        "chance": chance,
                        "avg_orbs": avg_orbs,
                        "min_ilvl": min_ilvl,
                        "source": source,
                    },
                )

                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported/updated {updated} rows into pool='{pool}'"
        ))

        if missing:
            self.stdout.write(self.style.WARNING(
                f"Missing {len(missing)} uniques not found in DB:"
            ))
            for m in missing[:20]:
                self.stdout.write(f"  - {m}")
            if len(missing) > 20:
                self.stdout.write("  ... (truncated)")
