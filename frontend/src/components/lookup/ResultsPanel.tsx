import type { SiteResult } from "../../types";
import { CATEGORIES, CATEGORY_COLORS } from "../../types";
import { ResultCard } from "./ResultCard";

interface Props {
  result: SiteResult;
  onRescan?: () => void;
}

export function ResultsPanel({ result, onRescan }: Props) {
  // Group detections by category
  const grouped: Record<string, typeof result.detections> = {};
  for (const d of result.detections) {
    if (!grouped[d.category]) grouped[d.category] = [];
    grouped[d.category].push(d);
  }

  const categories = Object.entries(grouped).sort(
    (a, b) => b[1].length - a[1].length
  );

  return (
    <div>
      {/* Site header */}
      <div className="bg-white rounded-lg border border-slate-200 p-6 mb-4">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">
              {result.domain}
            </h1>
            {result.title && (
              <p className="text-slate-500 mt-1">{result.title}</p>
            )}
          </div>
          {onRescan && (
            <button
              onClick={onRescan}
              className="text-sm text-blue-600 hover:text-blue-800 border border-blue-200 px-3 py-1.5 rounded hover:bg-blue-50 transition-colors"
            >
              Rescan
            </button>
          )}
        </div>

        <div className="flex flex-wrap gap-4 mt-4 text-sm text-slate-600">
          {result.icp_number && (
            <span className="bg-amber-50 text-amber-700 px-2 py-1 rounded text-xs">
              ICP: {result.icp_number}
            </span>
          )}
          {result.status_code && (
            <span>Status: {result.status_code}</span>
          )}
          {result.response_time_ms && (
            <span>{result.response_time_ms}ms</span>
          )}
          <span className="font-medium">
            {result.tech_count} technologies detected
          </span>
          {result.cached && (
            <span className="text-xs text-slate-400">(cached)</span>
          )}
        </div>

        {/* Category pills */}
        <div className="flex flex-wrap gap-2 mt-3">
          {categories.map(([cat, dets]) => (
            <span
              key={cat}
              className="text-xs px-2 py-1 rounded-full text-white"
              style={{ backgroundColor: CATEGORY_COLORS[cat] || "#94A3B8" }}
            >
              {CATEGORIES[cat] || cat} ({dets.length})
            </span>
          ))}
        </div>
      </div>

      {/* Detection groups */}
      {categories.map(([cat, dets]) => (
        <div
          key={cat}
          className="bg-white rounded-lg border border-slate-200 mb-3"
        >
          <div className="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
            <div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: CATEGORY_COLORS[cat] || "#94A3B8" }}
            />
            <h2 className="font-semibold text-slate-700 text-sm">
              {CATEGORIES[cat] || cat}
            </h2>
            <span className="text-xs text-slate-400">({dets.length})</span>
          </div>
          <div className="p-2">
            {dets.map((d) => (
              <ResultCard key={d.tech_slug} detection={d} />
            ))}
          </div>
        </div>
      ))}

      {result.detections.length === 0 && (
        <div className="bg-white rounded-lg border border-slate-200 p-8 text-center text-slate-500">
          No technologies detected. The site may be blocking automated requests.
        </div>
      )}
    </div>
  );
}
