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
    <form className="flex gap-3 mb-6">
      <input
        name="search"
        defaultValue={search}
        placeholder="Search unique or base item..."
        className="flex-1 px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      />

      <select
        name="ordering"
        defaultValue={ordering}
        className="px-3 py-2 border rounded-lg"
      >
        {sortOptions.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>

      <input type="hidden" name="league" value={league} />
      <input type="hidden" name="page" value="1" />

      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
      >
        Apply
      </button>
    </form>
  );
}
