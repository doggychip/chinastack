import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";
import type { TechnologyItem, SiteListItem } from "../types";
import { CATEGORIES, CATEGORY_COLORS } from "../types";

export function TechDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const [tech, setTech] = useState<TechnologyItem | null>(null);
  const [sites, setSites] = useState<SiteListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    setError(null);
    Promise.all([api.getTechnology(slug), api.getTechnologySites(slug)])
      .then(([t, s]) => {
        setTech(t);
        setSites(s);
      })
      .catch((e) => setError(e.message || "Failed to load technology"))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return <div className="text-center py-12 text-slate-500">Loading...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-600 bg-red-50 border border-red-200 rounded-lg p-4 max-w-md mx-auto">
          {error}
        </div>
      </div>
    );
  }

  if (!tech) {
    return (
      <div className="text-center py-12 text-slate-500">
        Technology not found.
      </div>
    );
  }

  const color = CATEGORY_COLORS[tech.category] || "#94A3B8";

  return (
    <div>
      <div className="bg-white rounded-lg border border-slate-200 p-6 mb-4">
        <div className="flex items-center gap-4">
          <div
            className="w-14 h-14 rounded-lg flex items-center justify-center text-white text-xl font-bold"
            style={{ backgroundColor: color }}
          >
            {tech.name.charAt(0)}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-800">{tech.name}</h1>
            <div className="flex items-center gap-2 mt-1">
              <span
                className="text-xs px-2 py-0.5 rounded-full text-white"
                style={{ backgroundColor: color }}
              >
                {CATEGORIES[tech.category] || tech.category}
              </span>
              <span className="text-sm text-slate-500">
                {tech.site_count} sites
              </span>
            </div>
          </div>
        </div>
        {tech.description && (
          <p className="text-slate-600 mt-3">{tech.description}</p>
        )}
        {tech.website && (
          <a
            href={tech.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-600 hover:underline mt-2 inline-block"
          >
            {tech.website}
          </a>
        )}
      </div>

      <h2 className="text-lg font-semibold text-slate-800 mb-3">
        Sites using {tech.name}
      </h2>

      <div className="bg-white rounded-lg border border-slate-200">
        {sites.map((s) => (
          <Link
            key={s.id}
            to={`/site/${s.domain}`}
            className="flex items-center justify-between px-4 py-3 border-b border-slate-50 hover:bg-slate-50 transition-colors"
          >
            <div>
              <span className="font-medium text-blue-600">{s.domain}</span>
              {s.title && (
                <span className="text-sm text-slate-400 ml-2">{s.title}</span>
              )}
            </div>
            <span className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded">
              {s.tech_count} techs
            </span>
          </Link>
        ))}

        {sites.length === 0 && (
          <div className="p-8 text-center text-slate-500">
            No sites detected yet.
          </div>
        )}
      </div>
    </div>
  );
}
