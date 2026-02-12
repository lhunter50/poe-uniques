type NavbarProps = {
  league: string;
};

export default function Navbar({ league }: NavbarProps) {
  return (
    <header className="border-b border-amber-700/25 bg-black/40">
      <div className="mx-auto max-w-6xl px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <div className="text-amber-200 font-semibold tracking-wide">
            PoE Uniques
          </div>

          <nav className="hidden md:flex items-center gap-4 text-sm text-zinc-200/80">
            <a className="hover:text-zinc-100 transition" href="/">Browse</a>
            <a className="hover:text-zinc-100 transition" href="/about">About</a>
            <a className="hover:text-zinc-100 transition" href="/api">API</a>
          </nav>
        </div>

        <div className="text-sm text-zinc-200/80">
          League: <span className="text-zinc-100">{league || "Current"}</span>
        </div>
      </div>
    </header>
  );
}
