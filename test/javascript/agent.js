// Minimal JS agent. Run with: node test/javascript/agent.js
// Requires: npm install ws

const WebSocket = require("ws");

const SERVER = process.env.SERVER || "ws://localhost:8000";
const NAME = process.env.NAME || `js-bot-${Math.floor(Math.random() * 1000)}`;

const ws = new WebSocket(`${SERVER}/ws/agent/${NAME}`);
let myId = null;
let nextDirChange = 0;

const send = (cmd, args = {}) => ws.send(JSON.stringify({ cmd, args }));

ws.on("open", () => console.log(`[${NAME}] connected`));
ws.on("message", (raw) => {
  const msg = JSON.parse(raw);
  if (msg.type === "joined") { myId = msg.id; return; }
  if (msg.type !== "state") return;

  const me = msg.players.find((p) => p.id === myId);
  if (!me || !me.alive) return;

  const enemies = msg.players.filter((p) => p.id !== myId && p.alive);
  if (enemies.length) {
    const t = enemies.reduce((a, b) =>
      (a.x - me.x) ** 2 + (a.y - me.y) ** 2 < (b.x - me.x) ** 2 + (b.y - me.y) ** 2 ? a : b
    );
    send("LOOK", { angle: Math.atan2(t.y - me.y, t.x - me.x) });
    send("SHOOT", { hold: true });
  }

  if (msg.now >= nextDirChange) {
    send("MOVE", { dx: Math.random() * 2 - 1, dy: Math.random() * 2 - 1 });
    nextDirChange = msg.now + 0.8 + Math.random();
  }
  if (me.ammo === 0 && !me.reloading) send("RELOAD");
});
ws.on("close", () => process.exit(0));
