import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { SiteListItem } from "../types";

export function SitesPage() {
  const [sites, setSites] = useState<SiteListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("tech_count");

  useEffect(() => {
    setLoading(true);
    api
      .listSites({ per_page: 100, q: query || undefined, sort })
      .then(setSites)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [query, sort]);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-4">Scanned Sites</h1>

      <div className="flex gap-3 mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search domains..."
          className="flex-1 bg-white border border-slate-200 rounded-lg px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="bg-white border border-slate-200 rounded-lg px-3 py-2 text-sm outline-none"
        >
          <option value="tech_count">Most Technologies</option>
          <option value="recent">Recently Scanned</option>
          <option value="domain">A-Z</option>
        </select>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500">Loading...</div>
      ) : (
        <div className="bg-white rounded-lg border border-slate-200">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-100 text-left text-slate-500">
                <th className="px-4 py-3 font-medium">Domain</th>
                <th className="px-4 py-3 font-medium hidden sm:table-cell">
                  Title
                </th>
                <th className="px-4 py-3 font-medium text-right">Tech</th>
                <th className="px-4 py-3 font-medium text-right hidden md:table-cell">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {sites.map((s) => (
                <tr
                  key={s.id}
                  className="border-b border-slate-50 hover:bg-slate-50 transition-colors"
                >
                  <td className="px-4 py-3">
                    <Link
                      to={`/site/${s.domain}`}
                      className="text-blue-600 hover:underline font-medium"
                    >
                      {s.domain}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-slate-500 truncate max-w-[200px] hidden sm:table-cell">
                    {s.title || "—"}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs font-medium">
                      {s.tech_count}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right text-slate-400 hidden md:table-cell">
                    {s.status_code || "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {sites.length === 0 && (
            <div className="p-8 text-center text-slate-500">
              No sites found. Scan some domains first!
            </div>
          )}
        </div>
      )}
    </div>
  );
}
