import { useEffect, useState, useRef } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api/client";
import type { TechnologyItem } from "../types";
import { CATEGORIES, CATEGORY_COLORS } from "../types";

export function TechnologiesPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [techs, setTechs] = useState<TechnologyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const selectedCategory = searchParams.get("category") || "";
  const debounceTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    debounceTimer.current = setTimeout(() => setDebouncedQuery(query), 300);
    return () => clearTimeout(debounceTimer.current);
  }, [query]);

  useEffect(() => {
    setLoading(true);
    setError(null);
    api
      .listTechnologies({
        category: selectedCategory || undefined,
        q: debouncedQuery || undefined,
      })
      .then(setTechs)
      .catch((e) => setError(e.message || "Failed to load technologies"))
      .finally(() => setLoading(false));
  }, [selectedCategory, debouncedQuery]);

  const categoryKeys = Object.keys(CATEGORIES);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Technologies</h1>

      {/* Category filters */}
      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={() => setSearchParams({})}
          className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
            !selectedCategory
              ? "bg-slate-800 text-white"
              : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
          }`}
        >
          All
        </button>
        {categoryKeys.map((key) => (
          <button
            key={key}
            onClick={() => setSearchParams({ category: key })}
            className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
              selectedCategory === key
                ? "text-white"
                : "bg-white border border-slate-200 text-slate-600 hover:bg-slate-50"
            }`}
            style={
              selectedCategory === key
                ? { backgroundColor: CATEGORY_COLORS[key] }
                : {}
            }
          >
            {CATEGORIES[key]}
          </button>
        ))}
      </div>

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search technologies..."
        className="w-full bg-white border border-slate-200 rounded-lg px-4 py-2 text-sm mb-4 outline-none focus:ring-2 focus:ring-blue-500"
      />

      {error && (
        <div className="mb-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-slate-500">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {techs.map((t) => (
            <Link
              key={t.slug}
              to={`/technologies/${t.slug}`}
              className="bg-white border border-slate-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all"
            >
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded flex items-center justify-center text-white text-sm font-bold shrink-0"
                  style={{
                    backgroundColor:
                      CATEGORY_COLORS[t.category] || "#94A3B8",
                  }}
                >
                  {t.name.charAt(0)}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-slate-800 text-sm truncate">
                    {t.name}
                  </div>
                  <div className="text-xs text-slate-500">
                    {CATEGORIES[t.category] || t.category}
                  </div>
                </div>
                <div className="text-right shrink-0">
                  <div className="text-sm font-bold text-slate-800">
                    {t.site_count}
                  </div>
                  <div className="text-xs text-slate-400">sites</div>
                </div>
              </div>
              {t.description && (
                <p className="text-xs text-slate-400 mt-2 truncate">
                  {t.description}
                </p>
              )}
            </Link>
          ))}
        </div>
      )}

      {!loading && !error && techs.length === 0 && (
        <div className="text-center py-12 text-slate-500">
          No technologies found.
        </div>
      )}
    </div>
  );
}
