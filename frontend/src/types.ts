export interface Wall { x: number; y: number; w: number; h: number }
export interface Spawn { x: number; y: number }

export interface InitMsg {
  type: "init";
  tick_rate: number;
  world: { width: number; height: number; walls: Wall[]; spawns: Spawn[] };
  weapons: Record<string, { damage: number; mag_size: number; fire_cooldown: number }>;
}

export interface PlayerState {
  id: number;
  name: string;
  x: number;
  y: number;
  angle: number;
  hp: number;
  alive: boolean;
  weapon: string;
  ammo: number;
  mag: number;
  aiming: boolean;
  reloading: boolean;
  kills: number;
  deaths: number;
  is_bot: boolean;
}

export interface ProjectileState {
  id: number;
  owner: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
}

export interface StateMsg {
  type: "state";
  tick: number;
  now: number;
  players: PlayerState[];
  projectiles: ProjectileState[];
}

export type ServerMsg = InitMsg | StateMsg | { type: string; [k: string]: unknown };
