type AncientMeta = {
  tier?: number | null;
  chance?: number | string | null;
  avg_orbs?: number | string | null;
  min_ilvl?: number | null;
};

function toNum(v: unknown): number | null {
  if (v == null) return null;
  const n = typeof v === "string" ? Number(v) : typeof v === "number" ? v : NaN;
  return Number.isFinite(n) ? n : null;
}

export function AncientMetaPanel({
  ancient,
  reserveSpace = true,
}: {
  ancient: AncientMeta | null | undefined;
  reserveSpace?: boolean;
}) {
  const tier = ancient?.tier != null ? `T${ancient.tier}` : null;
  const chance = toNum(ancient?.chance);
  const avg = toNum(ancient?.avg_orbs);
  const minIlvl = ancient?.min_ilvl ?? null;

  const chancePct = chance != null ? chance * 100 : null;
  const oneIn = chance != null && chance > 0 ? Math.round(1 / chance) : null;

  const show =
    ancient != null && (tier != null || chance != null || avg != null || minIlvl != null);

  const Wrapper = ({ children }: { children: React.ReactNode }) =>
    reserveSpace ? <div className="mt-3 min-h-23">{children}</div> : <div className="mt-3">{children}</div>;

  return (
    <Wrapper>
      {show ? (
        <div className="rounded border border-amber-700/30 bg-black/25 px-3 py-2 text-[12px] text-zinc-200">
          <div className="flex items-center justify-center gap-2">
            <span className="font-semibold text-amber-300/90">
              {tier ?? "—"}
            </span>

            <span className="text-zinc-500">•</span>

            <span className="text-zinc-300">
              Avg: {avg != null ? avg.toLocaleString() : "—"}
            </span>
          </div>

          <div className="mt-1 text-zinc-400">
            Chance:{" "}
            {chancePct != null ? (
              <>
                {chancePct.toFixed(4)}%{" "}
                {oneIn != null ? (
                  <span className="text-zinc-500">(≈ 1 in {oneIn.toLocaleString()})</span>
                ) : null}
              </>
            ) : (
              "—"
            )}
          </div>

          {minIlvl != null ? (
            <div className="mt-1 text-zinc-500">Min iLvl: {minIlvl}</div>
          ) : null}
        </div>
      ) : null}
    </Wrapper>
  );
}
