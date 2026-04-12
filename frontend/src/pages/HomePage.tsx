import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { SearchBar } from "../components/lookup/SearchBar";
import { api } from "../api/client";
import type { SiteResult, OverviewStats } from "../types";
import { CATEGORIES, CATEGORY_COLORS } from "../types";
import { ResultsPanel } from "../components/lookup/ResultsPanel";
import { useEffect } from "react";

export function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SiteResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [overview, setOverview] = useState<OverviewStats | null>(null);

  useEffect(() => {
    api.getOverview().then(setOverview).catch(() => {});
  }, []);

  const handleSearch = async (url: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await api.lookup(url);
      setResult(res);
    } catch (e: any) {
      setError(e.message || "Scan failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {!result && (
        <div className="max-w-2xl mx-auto pt-16 pb-12">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-slate-800 mb-2">
              <span className="text-[#10B981]">{"</>"}</span> ChinaStack
            </h1>
            <p className="text-slate-500 text-lg">
              建站雷达 — Discover what technologies Chinese websites are built
              with
            </p>
          </div>

          <SearchBar onSearch={handleSearch} loading={loading} size="large" />

          {error && (
            <div className="mt-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
              {error}
            </div>
          )}

          {/* Stats overview */}
          {overview && overview.total_sites > 0 && (
            <div className="mt-12">
              <div className="flex justify-center gap-8 mb-8 text-center">
                <div>
                  <div className="text-2xl font-bold text-slate-800">
                    {overview.total_sites}
                  </div>
                  <div className="text-xs text-slate-500">Sites Scanned</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-slate-800">
                    {overview.total_technologies}
                  </div>
                  <div className="text-xs text-slate-500">Technologies</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-slate-800">
                    {overview.total_detections}
                  </div>
                  <div className="text-xs text-slate-500">Detections</div>
                </div>
              </div>

              <h2 className="text-sm font-semibold text-slate-600 mb-3">
                Technology Categories
              </h2>
              <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
                {overview.categories.map((cat) => (
                  <button
                    key={cat.key}
                    onClick={() => navigate(`/technologies?category=${cat.key}`)}
                    className="bg-white border border-slate-200 rounded-lg p-3 text-center hover:border-blue-300 hover:shadow-sm transition-all"
                  >
                    <div
                      className="w-6 h-6 rounded mx-auto mb-1.5"
                      style={{
                        backgroundColor:
                          CATEGORY_COLORS[cat.key] || "#94A3B8",
                      }}
                    />
                    <div className="text-xs font-medium text-slate-700">
                      {cat.label}
                    </div>
                    <div className="text-xs text-slate-400">
                      {cat.tech_count}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {result && (
        <div>
          <div className="mb-4">
            <SearchBar onSearch={handleSearch} loading={loading} />
          </div>
          {error && (
            <div className="mb-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
              {error}
            </div>
          )}
          <ResultsPanel result={result} onRescan={() => handleSearch(result.url)} />
        </div>
      )}
    </div>
  );
}
