const sortOptions = [
  { label: "Name (A→Z)", value: "name" },
  { label: "Level (low→high)", value: "required_level" },
  { label: "Chaos value (high→low)", value: "-chaos_value" },
  { label: "Listings (high→low)", value: "-listing_count" },
];

export default function FiltersBar({
  league,
  search,
  ordering,
}: {
  league: string;
  search: string;
  ordering: string;
}) {
  return (
    <form className="w-full flex flex-wrap items-center gap-3">
      <input
        name="search"
        defaultValue={search}
        placeholder="Search unique or base item..."
        className="
          h-10 min-w-55 flex-1
          rounded-md
          bg-black/40
          border border-amber-700/30
          px-3 text-sm text-zinc-100
          placeholder:text-zinc-400/70
          outline-none
          focus:border-amber-500/60 focus:ring-2 focus:ring-amber-500/20
        "
      />

      <select
        name="ordering"
        defaultValue={ordering}
        className="
          h-10
          rounded-md
          bg-black/40
          border border-amber-700/30
          px-3 text-sm text-zinc-100
          outline-none
          focus:border-amber-500/60 focus:ring-2 focus:ring-amber-500/20
        "
      >
        {sortOptions.map((o) => (
          <option key={o.value} value={o.value} className="bg-zinc-950">
            {o.label}
          </option>
        ))}
      </select>

      <input type="hidden" name="league" value={league} />
      <input type="hidden" name="page" value="1" />

      <button
        type="submit"
        className="
          h-10 px-4
          rounded-md
          border border-amber-600/40
          bg-amber-600/20
          text-sm font-semibold text-amber-200
          hover:bg-amber-600/25 hover:border-amber-500/60
          transition
        "
      >
        Apply
      </button>
    </form>
  );
}
