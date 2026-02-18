import type { UniqueItem } from "@/lib/types";
import { PoEHeaderBar } from "./PoEHeaderBar";
import { PriceLine } from "./PriceLine";
import { AncientMetaPanel } from "./AncientMetaPanel";

export default function UniqueCard({ item }: { item: UniqueItem }) {
  const baseName = item.base_item?.name ?? "Unknown Base";
  const itemClass = item.base_item?.item_class ?? "item";
  const slot = item.base_item?.slot ?? "";
  const baseIcon = item.base_item?.icon_url ?? "";

  const chaos = item.chaos_value != null ? Number(item.chaos_value) : null;
  const divine = item.divine_value != null ? Number(item.divine_value) : null;

  const ancient = item.ancient_meta ?? null;

  const ancientTier = ancient?.tier != null ? `T${ancient.tier}` : null;
  const ancientChance = ancient?.chance != null ? Number(ancient.chance) : null;
  const ancientAvg = ancient?.avg_orbs != null ? Number(ancient.avg_orbs) : null;
  const ancientMinIlvl = ancient?.min_ilvl != null ? Number(ancient.min_ilvl) : null;

  const chancePct = ancientChance != null ? ancientChance * 100 : null;
  const oneIn =
    ancientChance != null && ancientChance > 0 ? Math.round(1 / ancientChance) : null;

  // Only show the ancient panel if it has something meaningful
  const showAncient =
    ancient != null &&
    (ancientTier != null ||
      ancientChance != null ||
      ancientAvg != null ||
      ancientMinIlvl != null);

  return (
    <div
      className="
        w-full
        max-w-105
        bg-[#0f1319]
        border border-amber-700/60
        shadow-[0_0_0_1px_rgba(0,0,0,0.6),0_16px_40px_rgba(0,0,0,0.55)]
        hover:-translate-y-px
        hover:shadow-[0_0_25px_rgba(245,158,11,0.18)]
        transition-all duration-150
      "
    >
      {/* Title bar */}
      <PoEHeaderBar title={item.name} subtitle={baseName} />

      {/* Body */}
      <div className="px-6 py-4 text-center">
        <div className="text-[14px] font-semibold text-zinc-200">
          {itemClass.toUpperCase()}
          {slot ? (
            <span className="text-zinc-400/80">
              {" "}
              • {slot.toUpperCase()}
            </span>
          ) : null}
        </div>

        <div className="mt-3 space-y-1 text-[13px] leading-snug text-[#7FB6FF]">
          <div>
            Required Level: <span>{item.required_level ?? "—"}</span>
          </div>

          <div>
            <PriceLine value={chaos} icon="chaos" />
          </div>

          <div>
            <PriceLine value={divine} icon="divine" />
          </div>

          <div>
            Listings: <span>{item.listing_count ?? "—"}</span>
          </div>
        </div>

        {/* Divider */}
        <div className="my-4 h-px w-full bg-amber-700/30" />

        {/* Larger Icon */}
        <div className="flex justify-center">
          <div
            className="
              relative
              h-28 w-28
              flex items-center justify-center
              bg-[#0b2a1f]
              border border-amber-700/40
            "
          >
            {item.image_url ? (
              <img
                src={item.image_url}
                alt={item.name}
                className="
                  max-h-[90%] max-w-[90%]
                  object-contain
                  drop-shadow-[0_0_8px_rgba(0,0,0,0.5)]
                "
              />
            ) : null}

            {/* Base icon overlay */}
            {baseIcon ? (
              <div className="absolute bottom-1 left-1 z-50 group">
                {/* Small icon */}
                <div
                  className="
                    h-9 w-9
                    rounded
                    bg-black/60
                    ring-1 ring-amber-700/40
                    flex items-center justify-center
                    overflow-hidden
                    cursor-zoom-in
                  "
                  title={baseName}
                >
                  <img
                    src={baseIcon}
                    alt={baseName}
                    className="h-[85%] w-[85%] object-contain"
                  />
                </div>

                {/* Hover tooltip */}
                <div
                  className="
                    absolute bottom-full left-1/2 -translate-x-1/2 mb-3
                    hidden group-hover:flex
                    flex-col items-center
                    w-32
                    px-3 py-3
                    bg-black/95
                    ring-1 ring-amber-600
                    shadow-xl shadow-black/70
                    rounded
                    z-999
                  "
                >
                  <img
                    src={baseIcon}
                    alt={baseName}
                    className="h-16 w-16 object-contain"
                  />

                  <div className="mt-2 text-[12px] text-amber-300 font-semibold text-center wrap-break-words">
                    {baseName}
                  </div>
                </div>
              </div>
            ) : null}

            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle,rgba(255,255,255,0.06),transparent_70%)]" />
          </div>
        </div>

        <div className="my-4 h-px w-full bg-amber-700/30" />

        <AncientMetaPanel ancient={item.ancient_meta ?? null} reserveSpace />
      </div>
    </div>
  );
}
