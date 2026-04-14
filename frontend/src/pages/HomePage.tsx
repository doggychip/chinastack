import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { SearchBar } from "../components/lookup/SearchBar";
import { api } from "../api/client";
import type { SiteResult, SiteListItem, OverviewStats, TopTech } from "../types";
import { CATEGORY_COLORS } from "../types";
import { ResultsPanel } from "../components/lookup/ResultsPanel";

export function HomePage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SiteResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [overview, setOverview] = useState<OverviewStats | null>(null);
  const [recent, setRecent] = useState<SiteListItem[]>([]);
  const [topTechs, setTopTechs] = useState<TopTech[]>([]);

  useEffect(() => {
    api.getOverview().then(setOverview).catch(() => {});
    api.recentSites(8).then(setRecent).catch(() => {});
    api.getTopTechnologies(10).then(setTopTechs).catch(() => {});
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
        <div className="max-w-3xl mx-auto pt-16 pb-12">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-slate-800 mb-2">
              <span className="text-[#10B981]">{"</>"}</span> ChinaStack
            </h1>
            <p className="text-slate-500 text-lg">
              建站雷达 — Discover what technologies Chinese websites are built
              with
            </p>
          </div>

          <div className="max-w-2xl mx-auto">
            <SearchBar
              onSearch={handleSearch}
              onInputChange={() => setError(null)}
              loading={loading}
              size="large"
            />
          </div>

          {error && (
            <div className="mt-4 max-w-2xl mx-auto text-red-600 bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
              {error}
            </div>
          )}

          {/* Stats overview */}
          {overview && overview.total_sites > 0 && (
            <div className="mt-12">
              <div className="flex justify-center gap-8 mb-8 text-center">
                <div>
                  <div className="text-2xl font-bold text-slate-800">
                    {overview.total_sites.toLocaleString()}
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
                    {overview.total_detections.toLocaleString()}
                  </div>
                  <div className="text-xs text-slate-500">Detections</div>
                </div>
              </div>

              {/* Two-column layout: Recent Scans + Top Technologies */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* Recent scans */}
                {recent.length > 0 && (
                  <div>
                    <h2 className="text-sm font-semibold text-slate-600 mb-3">
                      Recently Scanned
                    </h2>
                    <div className="bg-white rounded-lg border border-slate-200">
                      {recent.map((s) => (
                        <Link
                          key={s.id}
                          to={`/site/${s.domain}`}
                          className="flex items-center justify-between px-4 py-2.5 border-b border-slate-50 last:border-0 hover:bg-slate-50 transition-colors"
                        >
                          <span className="text-sm text-blue-600 font-medium truncate">
                            {s.domain}
                          </span>
                          <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded shrink-0 ml-2">
                            {s.tech_count}
                          </span>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Top technologies */}
                {topTechs.length > 0 && (
                  <div>
                    <h2 className="text-sm font-semibold text-slate-600 mb-3">
                      Top Technologies
                    </h2>
                    <div className="bg-white rounded-lg border border-slate-200">
                      {topTechs.map((t) => (
                        <Link
                          key={t.slug}
                          to={`/technologies/${t.slug}`}
                          className="flex items-center gap-3 px-4 py-2.5 border-b border-slate-50 last:border-0 hover:bg-slate-50 transition-colors"
                        >
                          <div
                            className="w-2 h-2 rounded-full shrink-0"
                            style={{
                              backgroundColor:
                                CATEGORY_COLORS[t.category] || "#94A3B8",
                            }}
                          />
                          <span className="text-sm text-slate-700 flex-1 truncate">
                            {t.name}
                          </span>
                          <span className="text-xs text-slate-400 shrink-0">
                            {t.percentage}%
                          </span>
                        </Link>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Category grid */}
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
          <ResultsPanel
            result={result}
            onRescan={() => handleSearch(result.url)}
          />
        </div>
      )}
    </div>
  );
}
