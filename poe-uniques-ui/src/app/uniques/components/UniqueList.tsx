import type { UniqueItem } from "../../../lib/types";
import UniqueCard from "./UniqueCard";

export default function UniqueList({ uniques }: { uniques: UniqueItem[] }){
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      {uniques.map((u) => (
        <UniqueCard key={u.id} item={u} />
      ))}
    </div>
  )
}