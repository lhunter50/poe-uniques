import type { UniqueItem } from "../../../lib/types";
import UniqueCard from "./UniqueCard";

export default function UniqueList({ uniques }: { uniques: UniqueItem[] }){
  return (
    <div className="
      grid gap-6
      grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
      justify-items-center
    ">
      {uniques.map((u) => (
        <UniqueCard key={u.id} item={u} />
      ))}
    </div>
  )
}