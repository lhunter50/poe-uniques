import type { UniqueItem } from "@/lib/types";

export default function UniqueCard({ item }: { item: UniqueItem }) {
  return (
    <div className="grid grid-cols-[56px_1fr_auto] gap-4 p-4 border rounded-xl items-center hover:shadow-sm transition">
      <div className="w-14 h-14 rounded-lg overflow-hidden bg-gray-100">
        {item.image_url && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={item.image_url}
            alt={item.name}
            className="w-full h-full object-cover"
          />
        )}
      </div>

      <div>
        <div className="font-semibold text-lg">{item.name}</div>
        <div className="text-sm text-gray-500 mt-1">
          Base: <span className="text-gray-800">{item.base_item?.name}</span>
          {" • "}
          {item.base_item?.item_class}
          {" • "}
          {item.base_item?.slot}
          {item.required_level != null && ` • Lv ${item.required_level}`}
        </div>
      </div>

      <div className="text-right tabular-nums">
        <div className="font-semibold">
          {item.chaos_value ? `${item.chaos_value}c` : "—"}
        </div>
        <div className="text-sm text-gray-500">
          {item.listing_count ?? "—"} listings
        </div>
      </div>
    </div>
  );
}
