import { useEffect, useRef, useState } from "react";
import type { InitMsg, StateMsg, ServerMsg } from "./types";

export type ConnState = "connecting" | "open" | "closed";

export function useArenaSocket() {
  const [conn, setConn] = useState<ConnState>("connecting");
  const [init, setInit] = useState<InitMsg | null>(null);
  const stateRef = useRef<StateMsg | null>(null);
  const [, force] = useState(0);

  useEffect(() => {
    const proto = location.protocol === "https:" ? "wss:" : "ws:";
    const url = `${proto}//${location.host}/ws/spectator`;
    let ws: WebSocket | null = null;
    let stopped = false;
    let retry = 0;

    const connect = () => {
      setConn("connecting");
      ws = new WebSocket(url);
      ws.onopen = () => { retry = 0; setConn("open"); };
      ws.onclose = () => {
        setConn("closed");
        if (!stopped) {
          retry = Math.min(retry + 1, 5);
          setTimeout(connect, 500 * retry);
        }
      };
      ws.onerror = () => ws?.close();
      ws.onmessage = (ev) => {
        const msg = JSON.parse(ev.data) as ServerMsg;
        if (msg.type === "init") setInit(msg as InitMsg);
        else if (msg.type === "state") {
          stateRef.current = msg as StateMsg;
          force((n) => (n + 1) & 0xffff);
        }
      };
    };
    connect();
    return () => { stopped = true; ws?.close(); };
  }, []);

  return { conn, init, state: stateRef.current };
}
