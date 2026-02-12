type PoEHeaderBarProps = {
  title: string;     // Unique name
  subtitle: string;  // Base item name
};

export function PoEHeaderBar({ title, subtitle }: PoEHeaderBarProps) {
  return (
    <div
      className="
        relative overflow-hidden
        border border-amber-700/60
        bg-zinc-950
        shadow-[0_0_0_1px_rgba(0,0,0,0.65)]
      "
    >
      {/* “Metal” texture-ish gradient */}
      <div
        className="
          absolute inset-0
          bg-[linear-gradient(180deg,rgba(255,255,255,0.06),rgba(0,0,0,0)_35%,rgba(0,0,0,0.35))]
        "
      />

      {/* Top + bottom inner lines */}
      <div className="absolute left-0 right-0 top-2 h-px bg-amber-700/35" />
      <div className="absolute left-0 right-0 bottom-2 h-px bg-amber-700/35" />

      {/* Center divider between title/subtitle */}
      <div className="absolute left-6 right-6 top-1/2 h-px -translate-y-1/2 bg-amber-700/25" />

      {/* Subtle vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.05),rgba(0,0,0,0)_60%)]" />

      {/* Content */}
      <div className="relative px-6 py-3 text-center">
        <div
          className="
            text-[18px] font-semibold tracking-wide text-amber-300
            [text-shadow:0_0_10px_rgba(245,158,11,0.18)]
          "
        >
          {title.toUpperCase()}
        </div>
        <div
          className="
            -mt-1 text-[16px] font-semibold tracking-wide text-amber-300/90
            [text-shadow:0_0_10px_rgba(245,158,11,0.14)]
          "
        >
          {subtitle.toUpperCase()}
        </div>
      </div>

      {/* Corner “ornaments” */}
      <div className="pointer-events-none absolute left-0 top-0 h-full w-10 bg-[linear-gradient(90deg,rgba(180,83,9,0.35),rgba(0,0,0,0))]" />
      <div className="pointer-events-none absolute right-0 top-0 h-full w-10 bg-[linear-gradient(270deg,rgba(180,83,9,0.35),rgba(0,0,0,0))]" />
    </div>
  );
}
