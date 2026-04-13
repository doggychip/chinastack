import { Link, useLocation } from "react-router-dom";

export function Header() {
  const location = useLocation();

  const links = [
    { to: "/", label: "Search", exact: true },
    { to: "/sites", label: "Sites" },
    { to: "/technologies", label: "Technologies" },
    { to: "/stats", label: "Stats" },
  ];

  const isActive = (link: typeof links[number]) => {
    if (link.exact) return location.pathname === link.to;
    if (link.to === "/sites") return location.pathname.startsWith("/site");
    return location.pathname.startsWith(link.to);
  };

  return (
    <header className="bg-[#0F172A] text-white">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2 font-bold text-lg">
          <span className="text-[#10B981]">{"</>"}</span>
          <span>ChinaStack</span>
          <span className="text-xs text-slate-400 font-normal hidden sm:inline">
            建站雷达
          </span>
        </Link>

        <nav className="flex gap-1">
          {links.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className={`px-3 py-1.5 rounded text-sm transition-colors ${
                isActive(l)
                  ? "bg-white/10 text-white"
                  : "text-slate-300 hover:text-white hover:bg-white/5"
              }`}
            >
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
