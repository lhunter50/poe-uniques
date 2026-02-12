export function compactNumber(input: string | number | null | undefined): string {
  if (input == null) return "—";

  const n = typeof input === "string" ? Number(input) : input;
  if (!Number.isFinite(n)) return "—";

  const abs = Math.abs(n);

  // < 1000: show up to 2 decimals, but trim trailing zeros
  if (abs < 1000) {
    const s = n.toFixed(2);
    return s.replace(/\.?0+$/, "");
  }

  // 1K+
  const units: Array<{ v: number; s: string }> = [
    { v: 1e12, s: "T" },
    { v: 1e9, s: "B" },
    { v: 1e6, s: "M" },
    { v: 1e3, s: "K" },
  ];

  const u = units.find((x) => abs >= x.v)!;
  const value = n / u.v;

  // Big numbers: fewer decimals
  const decimals = abs >= 1e6 ? 2 : 2; 
  const s = value.toFixed(decimals).replace(/\.?0+$/, "");
  return `${s}${u.s}`;
}
