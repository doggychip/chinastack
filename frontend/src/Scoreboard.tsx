import type { PlayerState } from "./types";

export function Scoreboard({ players }: { players: PlayerState[] }) {
  const ranked = [...players].sort(
    (a, b) => b.kills - a.kills || a.deaths - b.deaths || a.name.localeCompare(b.name)
  );
  return (
    <div className="rounded-lg border border-zinc-800 bg-zinc-900/60 p-4 w-full">
      <h2 className="text-sm font-semibold uppercase tracking-wider text-zinc-400 mb-3">
        Scoreboard
      </h2>
      <table className="w-full text-sm">
        <thead className="text-zinc-500 text-xs uppercase">
          <tr>
            <th className="text-left font-medium pb-2">Name</th>
            <th className="text-right font-medium pb-2">K</th>
            <th className="text-right font-medium pb-2">D</th>
            <th className="text-right font-medium pb-2">HP</th>
            <th className="text-right font-medium pb-2">Weapon</th>
          </tr>
        </thead>
        <tbody>
          {ranked.map((p) => (
            <tr key={p.id} className="border-t border-zinc-800/60">
              <td className="py-1.5">
                <span
                  className={`inline-block w-2 h-2 rounded-full mr-2 ${
                    p.alive ? (p.is_bot ? "bg-red-400" : "bg-cyan-400") : "bg-zinc-600"
                  }`}
                />
                <span className={p.alive ? "text-zinc-100" : "text-zinc-500"}>{p.name}</span>
                {p.is_bot && (
                  <span className="ml-2 text-[10px] uppercase tracking-wider text-zinc-500">bot</span>
                )}
              </td>
              <td className="text-right tabular-nums">{p.kills}</td>
              <td className="text-right tabular-nums text-zinc-400">{p.deaths}</td>
              <td className="text-right tabular-nums text-zinc-400">{p.alive ? p.hp.toFixed(0) : "—"}</td>
              <td className="text-right text-zinc-400 text-xs">
                {p.weapon} <span className="text-zinc-600">{p.ammo}/{p.mag}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
