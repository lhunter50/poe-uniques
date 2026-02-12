import { getUniques } from "@/lib/api";
import { qp } from "@/lib/query";
import FiltersBar from "./uniques/controls/FiltersBar";
import Pagination from "./uniques/controls/Pagination";
import UniqueList from "./uniques/components/UniqueList";

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const params = await searchParams;

  const page = qp(params.page) ?? "1";
  const search = qp(params.search) ?? "";
  const ordering = qp(params.ordering) ?? "name";
  const league = qp(params.league) ?? ""; // empty = backend uses current league

  const data = await getUniques({ page, search, ordering, league });

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      {/* vignette + subtle top fade */}
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.06),rgba(0,0,0,0)_55%)]" />
      <div className="pointer-events-none fixed inset-0 bg-[linear-gradient(180deg,rgba(0,0,0,0.70),rgba(0,0,0,0)_35%)]" />

      <main className="relative mx-auto max-w-6xl px-4 py-8">
        {/* Header + controls panel */}
        <div
          className="
            mb-6 overflow-hidden rounded-lg
            bg-zinc-950/70
            border border-amber-700/35
            shadow-[0_0_0_1px_rgba(0,0,0,0.6),0_16px_40px_rgba(0,0,0,0.45)]
          "
        >
          <div className="px-5 py-4">
            <h1 className="text-2xl font-semibold tracking-wide text-amber-200">
              PoE Uniques
            </h1>

            <p className="mt-1 text-sm text-zinc-300/80">
              Showing {data.results.length} of {data.count} (League:{" "}
              {league || "Current"})
            </p>

            <div className="mt-4">
              <FiltersBar league={league} search={search} ordering={ordering} />
            </div>
          </div>

          <div className="h-px bg-amber-700/25" />
        </div>

        {/* Grid panel (optional but looks cohesive) */}
        <div className="rounded-lg border border-amber-700/15 bg-black/20 p-4">
          <UniqueList uniques={data.results} />
        </div>

        <div className="mt-6">
          <Pagination
            page={Number(page)}
            hasPrev={!!data.previous}
            hasNext={!!data.next}
            league={league}
            search={search}
            ordering={ordering}
          />
        </div>
      </main>
    </div>
  );
}
