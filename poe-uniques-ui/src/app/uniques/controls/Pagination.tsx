function buildHref(params: {
  page: number;
  league: string;
  search: string;
  ordering: string;
}) {
  const qs = new URLSearchParams();
  qs.set("page", String(params.page));
  qs.set("league", params.league);
  if (params.search) qs.set("search", params.search);
  if (params.ordering) qs.set("ordering", params.ordering);
  return `/?${qs.toString()}`;
}

export default function Pagination({
  page,
  hasPrev,
  hasNext,
  league,
  search,
  ordering,
}: {
  page: number;
  hasPrev: boolean;
  hasNext: boolean;
  league: string;
  search: string;
  ordering: string;
}) {
  return (
    <div className="flex items-center gap-4 mt-6">
      {hasPrev ? (
        <a
          href={buildHref({ page: Math.max(1, page - 1), league, search, ordering })}
          className="text-blue-600 hover:underline"
        >
          ← Prev
        </a>
      ) : (
        <span className="text-gray-400">← Prev</span>
      )}

      <span className="text-gray-600">Page {page}</span>

      {hasNext ? (
        <a
          href={buildHref({ page: page + 1, league, search, ordering })}
          className="text-blue-600 hover:underline"
        >
          Next →
        </a>
      ) : (
        <span className="text-gray-400">Next →</span>
      )}
    </div>
  );
}
