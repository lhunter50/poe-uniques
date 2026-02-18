import type { Paginated, UniqueItem, UniqueQuery } from "./types";

function getApiBase(): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;
  if(!base) {
    throw new Error("Missing url in .env.local");
  }
  return base.replace(/\/+$/, "");
};

export async function getUniques(params:UniqueQuery): Promise<Paginated<UniqueItem>> {
  const base = getApiBase();
  const qs = new URLSearchParams();

  if (params.league) qs.set("league", params.league);
  qs.set("page", params.page ?? "1");

  if (params.search) qs.set("search", params.search);
  if (params.ordering) qs.set("ordering", params.ordering);

  const url = `${base}/api/uniques/?${qs.toString()}`;

  const res = await fetch(url, { next: { revalidate: 60 * 30 }, });
  if (!res.ok) {
    throw new Error(`Failed to fetch uniques: ${res.status} ${res.statusText}`)
  }
  return res.json();
}