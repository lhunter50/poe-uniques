import { getUniques } from "@/lib/api";
import { qp } from "@/lib/query";
import UniqueList from "./uniques/components/UniqueList";
import Pagination from "./uniques/controls/Pagination";

import PageShell from "@/app/layout/PageShell";
import Navbar from "@/app/layout/Navbar";
import SearchStrip from "@/app/layout/SearchStrip";

export default async function Home({
  searchParams,
}: {
  searchParams: { [key: string]: string | string[] | undefined };
}) {
  const params = await searchParams;

  const page = qp(params.page) ?? "1";
  const search = qp(params.search) ?? "";
  const ordering = qp(params.ordering) ?? "name";
  const league = qp(params.league) ?? "";

  const data = await getUniques({ page, search, ordering, league });

  return (
    <PageShell>
      <Navbar league={league} />

      <SearchStrip
        shown={data.results.length}
        total={data.count}
        league={league}
        search={search}
        ordering={ordering}
      />

      <main className="mx-auto max-w-6xl px-4 py-6">
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
    </PageShell>
  );
}
