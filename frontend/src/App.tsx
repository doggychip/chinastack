import { Arena } from "./Arena";
import { Scoreboard } from "./Scoreboard";
import { useArenaSocket } from "./useArenaSocket";

export default function App() {
  const { conn, init, state } = useArenaSocket();
  const players = state?.players ?? [];

  return (
    <div className="min-h-screen w-full bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-lg font-semibold tracking-tight">AI Battle Arena</div>
          <span className="text-xs text-zinc-500">
            programmatic-only · WebSocket command API
          </span>
        </div>
        <div className="flex items-center gap-4 text-xs text-zinc-400">
          <span>tick {state?.tick ?? 0}</span>
          <span className="flex items-center gap-1.5">
            <span
              className={`inline-block w-2 h-2 rounded-full ${
                conn === "open" ? "bg-emerald-400" : conn === "connecting" ? "bg-amber-400" : "bg-red-400"
              }`}
            />
            {conn}
          </span>
        </div>
      </header>

      <main className="p-6 grid gap-6 lg:grid-cols-[1fr_320px] max-w-[1700px] mx-auto">
        <div className="flex items-start justify-center">
          {init ? (
            <Arena init={init} state={state} />
          ) : (
            <div className="text-zinc-500 text-sm">Loading arena…</div>
          )}
        </div>
        <aside className="space-y-4">
          <Scoreboard players={players} />
          <div className="rounded-lg border border-zinc-800 bg-zinc-900/60 p-4 text-xs text-zinc-400 leading-relaxed">
            <h3 className="text-zinc-300 text-sm font-semibold mb-2">Connect an agent</h3>
            <code className="block bg-zinc-950/70 border border-zinc-800 rounded p-2 text-[11px] text-zinc-300">
              ws://localhost:8000/ws/agent/&lt;name&gt;
            </code>
            <p className="mt-2">
              Send JSON commands: <code>MOVE</code>, <code>LOOK</code>, <code>SHOOT</code>,{" "}
              <code>RELOAD</code>, <code>SWITCH_WEAPON</code>, <code>AIM</code>.
            </p>
            <p className="mt-1">
              Sample agents in <code>test/python/</code>.
            </p>
          </div>
        </aside>
      </main>
    </div>
  );
}
