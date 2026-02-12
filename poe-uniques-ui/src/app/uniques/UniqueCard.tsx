import type { UniqueItem } from "@/lib/types";
import { PoEHeaderBar } from "./PoEHeaderBar";

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
        bg-zinc-950/95
        border border-amber-700/60
        shadow-[0_0_0_1px_rgba(0,0,0,0.6),0_16px_40px_rgba(0,0,0,0.55)]
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
            Chaos Value:{" "}
            <span>
              {chaos != null ? chaos.toFixed(2) : "—"}
            </span>{" "}
            c
          </div>

          <div>
            Divine Value:{" "}
            <span>
              {divine != null ? divine.toFixed(2) : "—"}
            </span>{" "}
            d
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
          <div className="h-28 w-28 bg-emerald-900/40 border border-amber-700/30 grid place-items-center">
            {item.image_url ? (
              <img
                src={item.image_url}
                alt={item.name}
                className="h-24 w-24 object-contain"
              />
            ) : (
              <div className="h-16 w-16 rounded bg-zinc-700/50" />
            )}
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
