import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { OverviewStats, TopTech, CategoryDetail } from "../types";
import { CATEGORY_COLORS } from "../types";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export function StatsPage() {
  const [overview, setOverview] = useState<OverviewStats | null>(null);
  const [topTechs, setTopTechs] = useState<TopTech[]>([]);
  const [selectedCat, setSelectedCat] = useState<string | null>(null);
  const [catDetail, setCatDetail] = useState<CategoryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    Promise.all([api.getOverview(), api.getTopTechnologies(20)])
      .then(([o, t]) => {
        setOverview(o);
        setTopTechs(t);
      })
      .catch((e) => setError(e.message || "Failed to load stats"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (!selectedCat) {
      setCatDetail(null);
      return;
    }
    api.getCategoryStats(selectedCat).then(setCatDetail).catch(() => {});
  }, [selectedCat]);

  if (loading) {
    return <div className="text-center py-12 text-slate-500">Loading...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-slate-800 mb-4">
          Market Statistics
        </h1>
        <div className="text-red-600 bg-red-50 border border-red-200 rounded-lg p-4 max-w-md mx-auto">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">
        Market Statistics
      </h1>

      {/* Overview counters */}
      {overview && (
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-lg border border-slate-200 p-4 text-center">
            <div className="text-3xl font-bold text-slate-800">
              {overview.total_sites}
            </div>
            <div className="text-sm text-slate-500">Sites Scanned</div>
          </div>
          <div className="bg-white rounded-lg border border-slate-200 p-4 text-center">
            <div className="text-3xl font-bold text-slate-800">
              {overview.total_technologies}
            </div>
            <div className="text-sm text-slate-500">Technologies Tracked</div>
          </div>
          <div className="bg-white rounded-lg border border-slate-200 p-4 text-center">
            <div className="text-3xl font-bold text-slate-800">
              {overview.total_detections}
            </div>
            <div className="text-sm text-slate-500">Total Detections</div>
          </div>
        </div>
      )}

      {/* Top technologies chart */}
      <div className="bg-white rounded-lg border border-slate-200 p-6 mb-6">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Top Technologies
        </h2>
        {topTechs.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart
              data={topTechs}
              layout="vertical"
              margin={{ left: 120, right: 20 }}
            >
              <XAxis type="number" />
              <YAxis
                type="category"
                dataKey="name"
                tick={{ fontSize: 12 }}
                width={120}
              />
              <Tooltip
                formatter={(value: number, _name: string, props: any) => [
                  `${value} sites (${props.payload.percentage}%)`,
                  props.payload.category_label,
                ]}
              />
              <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                {topTechs.map((t, i) => (
                  <Cell
                    key={i}
                    fill={CATEGORY_COLORS[t.category] || "#94A3B8"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-8 text-slate-400">
            No data yet. Scan some sites first!
          </div>
        )}
      </div>

      {/* Category breakdown */}
      <div className="bg-white rounded-lg border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-800 mb-4">
          Market Share by Category
        </h2>

        {overview && overview.categories.length > 0 ? (
          <>
            <div className="flex flex-wrap gap-2 mb-4">
              {overview.categories.map((cat) => (
                <button
                  key={cat.key}
                  onClick={() =>
                    setSelectedCat(selectedCat === cat.key ? null : cat.key)
                  }
                  className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                    selectedCat === cat.key
                      ? "text-white"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                  style={
                    selectedCat === cat.key
                      ? { backgroundColor: CATEGORY_COLORS[cat.key] }
                      : {}
                  }
                >
                  {cat.label}
                </button>
              ))}
            </div>

            {catDetail ? (
              <div>
                <h3 className="font-medium text-slate-700 mb-3">
                  {catDetail.category_label} Market Share
                </h3>
                {catDetail.technologies.length > 0 ? (
                  <div className="space-y-2">
                    {catDetail.technologies.map((t) => (
                      <div key={t.slug} className="flex items-center gap-3">
                        <span className="w-32 text-sm text-slate-700 truncate">
                          {t.name}
                        </span>
                        <div className="flex-1 bg-slate-100 rounded-full h-5 overflow-hidden">
                          <div
                            className="h-full rounded-full transition-all"
                            style={{
                              width: `${Math.max(t.percentage, 2)}%`,
                              backgroundColor:
                                CATEGORY_COLORS[catDetail.category] || "#94A3B8",
                            }}
                          />
                        </div>
                        <span className="text-sm text-slate-500 w-20 text-right">
                          {t.count} ({t.percentage}%)
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-4 text-slate-400">
                    No data for this category yet.
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-4 text-slate-400">
                Select a category to see market share breakdown.
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-4 text-slate-400">
            No category data available.
          </div>
        )}
      </div>
    </div>
  );
}
