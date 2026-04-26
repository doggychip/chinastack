import { useEffect, useRef } from "react";
import type { InitMsg, StateMsg } from "./types";

interface Props {
  init: InitMsg;
  state: StateMsg | null;
}

const PLAYER_RADIUS = 14;
const PROJECTILE_RADIUS = 3;

export function Arena({ init, state }: Props) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = init.world.width;
    const H = init.world.height;

    const draw = () => {
      ctx.fillStyle = "#0a0a0b";
      ctx.fillRect(0, 0, W, H);

      ctx.strokeStyle = "#18181b";
      ctx.lineWidth = 1;
      for (let x = 0; x <= W; x += 32) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
      }
      for (let y = 0; y <= H; y += 32) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
      }

      ctx.fillStyle = "#3f3f46";
      ctx.strokeStyle = "#52525b";
      for (const wall of init.world.walls) {
        ctx.fillRect(wall.x, wall.y, wall.w, wall.h);
        ctx.strokeRect(wall.x + 0.5, wall.y + 0.5, wall.w - 1, wall.h - 1);
      }

      if (state) {
        ctx.fillStyle = "#facc15";
        for (const p of state.projectiles) {
          ctx.beginPath();
          ctx.arc(p.x, p.y, PROJECTILE_RADIUS, 0, Math.PI * 2);
          ctx.fill();
        }

        for (const p of state.players) {
          if (!p.alive) {
            ctx.fillStyle = "#52525b";
            ctx.beginPath();
            ctx.arc(p.x, p.y, PLAYER_RADIUS, 0, Math.PI * 2);
            ctx.fill();
            continue;
          }

          const color = p.is_bot ? "#ef4444" : "#22d3ee";
          ctx.fillStyle = color;
          ctx.beginPath();
          ctx.arc(p.x, p.y, PLAYER_RADIUS, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = "#0b0b0c";
          ctx.lineWidth = 2;
          ctx.stroke();

          ctx.strokeStyle = color;
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(
            p.x + Math.cos(p.angle) * (PLAYER_RADIUS + 10),
            p.y + Math.sin(p.angle) * (PLAYER_RADIUS + 10)
          );
          ctx.stroke();

          const barW = 28;
          const barH = 4;
          const bx = p.x - barW / 2;
          const by = p.y - PLAYER_RADIUS - 10;
          ctx.fillStyle = "#27272a";
          ctx.fillRect(bx, by, barW, barH);
          ctx.fillStyle = p.hp > 50 ? "#22c55e" : p.hp > 25 ? "#eab308" : "#ef4444";
          ctx.fillRect(bx, by, (barW * p.hp) / 100, barH);

          ctx.fillStyle = "#e4e4e7";
          ctx.font = "11px ui-sans-serif, system-ui";
          ctx.textAlign = "center";
          ctx.fillText(p.name, p.x, p.y - PLAYER_RADIUS - 14);
        }
      }
    };

    let raf = 0;
    const loop = () => {
      draw();
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [init, state]);

  return (
    <canvas
      ref={canvasRef}
      width={init.world.width}
      height={init.world.height}
      className="border border-zinc-800 rounded-lg shadow-2xl max-w-full h-auto"
    />
  );
}
