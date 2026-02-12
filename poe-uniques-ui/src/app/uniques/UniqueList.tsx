import type { UniqueItem } from "../../lib/types";
import UniqueCard from "./UniqueCard";

export default function UniqueList({ uniques }: { uniques: UniqueItem[] }){
  return (
    <div className="grid gap-4">
      {uniques.map((u) => (
        <UniqueCard key={u.id} item={u} />
      ))}
    </div>
  )
}