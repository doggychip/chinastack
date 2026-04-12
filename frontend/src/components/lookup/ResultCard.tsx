import type { Detection } from "../../types";
import { CATEGORY_COLORS } from "../../types";

interface Props {
  detection: Detection;
}

export function ResultCard({ detection }: Props) {
  const color = CATEGORY_COLORS[detection.category] || "#94A3B8";

  return (
    <div className="flex items-start gap-3 py-2.5 px-3 rounded-lg hover:bg-slate-50 transition-colors">
      <div
        className="w-8 h-8 rounded flex items-center justify-center text-white text-xs font-bold shrink-0 mt-0.5"
        style={{ backgroundColor: color }}
      >
        {detection.tech_name.charAt(0)}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-slate-800 text-sm">
            {detection.tech_name}
          </span>
          {detection.version && (
            <span className="text-xs text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded">
              v{detection.version}
            </span>
          )}
        </div>
        {detection.description && (
          <p className="text-xs text-slate-500 mt-0.5">{detection.description}</p>
        )}
        {detection.evidence && (
          <p className="text-xs text-slate-400 mt-1 font-mono truncate">
            {detection.evidence}
          </p>
        )}
      </div>
      <div className="text-xs text-slate-400 shrink-0">
        {Math.round(detection.confidence * 100)}%
      </div>
    </div>
  );
}
