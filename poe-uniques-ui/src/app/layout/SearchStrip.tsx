import FiltersBar from "@/app/uniques/controls/FiltersBar";

type SearchStripProps = {
  shown: number;
  total: number;
  league: string;
  search: string;
  ordering: string;
};

export default function SearchStrip({
  shown,
  total,
  league,
  search,
  ordering,
}: SearchStripProps) {
  return (
    <section className="border-b border-amber-700/20 bg-[#10141a]/80">
      <div className="mx-auto max-w-6xl px-4 py-4">
        <div className="text-sm text-zinc-300/80 mb-3">
          Showing {shown} of {total}
        </div>

        <FiltersBar
          league={league}
          search={search}
          ordering={ordering}
        />
      </div>
    </section>
  );
}
