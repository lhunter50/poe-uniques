import type { UniqueItem } from "@/lib/types";
import { PoEHeaderBar } from "./PoEHeaderBar";
import { compactNumber } from "@/lib/format";
import { PriceLine } from "./PriceLine";

export default function UniqueCard({ item }: { item: UniqueItem }) {
  const baseName = item.base_item?.name ?? "Unknown Base";
  const itemClass = item.base_item?.item_class ?? "item";
  const slot = item.base_item?.slot ?? "";

  const chaos = item.chaos_value != null ? Number(item.chaos_value) : null;
  const divine = item.divine_value != null ? Number(item.divine_value) : null;

  return (
    <div
      className="
        w-full max-w-105
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
          {String(itemClass).toUpperCase()}
          {slot ? <span className="text-zinc-400/80">{" • "}{String(slot).toUpperCase()}</span> : null}
        </div>

        <div className="mt-3 space-y-1 text-[13px] leading-snug text-[#7FB6FF]">
          <div>
            Required Level:{" "}
            <span>
              {item.required_level ?? "—"}
            </span>
          </div>

          <div>
            <PriceLine value={chaos} icon="chaos" />
          </div>

          <div>
            <PriceLine value={divine} icon="divine"/>
          </div>

          <div>
            Listings:{" "}
            <span>
              {item.listing_count ?? "—"}
            </span>
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
              overflow-hidden
            "
          >
            {item.image_url ? (
              <img
                src={item.image_url}
                alt={item.name}
                className="
                  max-h-[90%] max-w-[90%]
                  object-contain
                  image-rendering-auto
                  drop-shadow-[0_0_8px_rgba(0,0,0,0.5)]
                "
              />
            ) : null}
              <div className="absolute inset-0 bg-[radial-gradient(circle,rgba(255,255,255,0.06),transparent_70%)]" />
          </div>
        </div>

        {/* Flavour Text (under image like PoE) */}
        {item.flavour_text && (
          <>
            <div className="my-4 h-px w-full bg-amber-700/30" />
            <div className="text-[13px] italic tracking-wide text-amber-300/90">
              {item.flavour_text}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
