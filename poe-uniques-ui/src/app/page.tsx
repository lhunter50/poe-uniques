import { getUniques } from "@/lib/api";
import { qp } from "@/lib/query";
import FiltersBar from "./uniques/controls/FiltersBar";
import Pagination from "./uniques/controls/Pagination";
import UniqueList from "./uniques/UniqueList";

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
    <main className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">PoE Uniques</h1>

      <p className="text-gray-500 mb-4">
        Showing {data.results.length} of {data.count} (League: {league || "Current"})
      </p>

      <FiltersBar league={league} search={search} ordering={ordering} />

      <UniqueList uniques={data.results} />

      <Pagination
        page={Number(page)}
        hasPrev={!!data.previous}
        hasNext={!!data.next}
        league={league}
        search={search}
        ordering={ordering}
      />
    </main>
  );
}
