type NavbarProps = {
  league: string;
};

export default function Navbar({ league }: NavbarProps) {
  return (
    <header
      className="
        border-b border-amber-700/30
        bg-[#11161d]/90
        backdrop-blur-sm
        shadow-[0_4px_20px_rgba(0,0,0,0.4)]
        after:absolute after:top-0 after:left-0 after:right-0
        after:h-px after:bg-amber-500/30
      "
    >
      <div className="mx-auto max-w-6xl px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <div className="text-xl font-semibold tracking-wide text-amber-200">
            PoE Uniques
          </div>

          <nav className="hidden md:flex items-center gap-6 text-base text-zinc-200/90">
            <a
              className="hover:text-white transition"
              href="/"
            >
              Browse
            </a>
            <a
              className="hover:text-white transition"
              href="/about"
            >
              About
            </a>
            <a
              className="hover:text-white transition"
              href="/api"
            >
              API
            </a>
          </nav>
        </div>

        <div className="text-sm text-zinc-300">
          League:{" "}
          <span className="text-zinc-100 font-medium">
            {league || "Current"}
          </span>
        </div>
      </div>
    </header>
  );
}
