const API_BASE = import.meta.env.VITE_API_URL || "";

async function fetchJSON<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body ? `${res.status}: ${body}` : `${res.status} ${res.statusText || "Request failed"}`);
  }
  return res.json();
}

import type {
  SiteResult,
  SiteListItem,
  TechnologyItem,
  OverviewStats,
  TopTech,
  CategoryDetail,
} from "../types";

export const api = {
  lookup(url: string) {
    return fetchJSON<SiteResult>("/api/lookup", {
      method: "POST",
      body: JSON.stringify({ url }),
    });
  },

  getCachedLookup(domain: string) {
    return fetchJSON<SiteResult>(`/api/lookup/${encodeURIComponent(domain)}`);
  },

  recentSites(limit = 10) {
    return fetchJSON<SiteListItem[]>(`/api/sites/recent?limit=${limit}`);
  },

  listSites(params?: { page?: number; per_page?: number; q?: string; sort?: string }) {
    const sp = new URLSearchParams();
    if (params?.page) sp.set("page", String(params.page));
    if (params?.per_page) sp.set("per_page", String(params.per_page));
    if (params?.q) sp.set("q", params.q);
    if (params?.sort) sp.set("sort", params.sort);
    return fetchJSON<SiteListItem[]>(`/api/sites?${sp}`);
  },

  getSite(domain: string) {
    return fetchJSON<SiteResult>(`/api/sites/${encodeURIComponent(domain)}`);
  },

  listTechnologies(params?: { category?: string; q?: string }) {
    const sp = new URLSearchParams();
    if (params?.category) sp.set("category", params.category);
    if (params?.q) sp.set("q", params.q);
    return fetchJSON<TechnologyItem[]>(`/api/technologies?${sp}`);
  },

  getTechnology(slug: string) {
    return fetchJSON<TechnologyItem>(`/api/technologies/${slug}`);
  },

  getTechnologySites(slug: string, page = 1) {
    return fetchJSON<SiteListItem[]>(`/api/technologies/${slug}/sites?page=${page}`);
  },

  getOverview() {
    return fetchJSON<OverviewStats>("/api/stats/overview");
  },

  getTopTechnologies(limit = 20) {
    return fetchJSON<TopTech[]>(`/api/stats/top-technologies?limit=${limit}`);
  },

  getCategoryStats(category: string) {
    return fetchJSON<CategoryDetail>(`/api/stats/category/${category}`);
  },

  exportSitesUrl(params?: { tech?: string; category?: string; q?: string }) {
    const sp = new URLSearchParams();
    if (params?.tech) sp.set("tech", params.tech);
    if (params?.category) sp.set("category", params.category);
    if (params?.q) sp.set("q", params.q);
    return `${API_BASE}/api/export/sites?${sp}`;
  },

  exportTechnologiesUrl(category?: string) {
    const sp = new URLSearchParams();
    if (category) sp.set("category", category);
    return `${API_BASE}/api/export/technologies?${sp}`;
  },
};
