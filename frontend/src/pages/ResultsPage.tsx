import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import type { SiteResult } from "../types";
import { ResultsPanel } from "../components/lookup/ResultsPanel";
import { SearchBar } from "../components/lookup/SearchBar";

export function ResultsPage() {
  const { domain } = useParams<{ domain: string }>();
  const [result, setResult] = useState<SiteResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    if (!domain) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.getCachedLookup(domain);
      setResult(res);
    } catch {
      // Not cached, do a fresh scan
      try {
        const res = await api.lookup(domain);
        setResult(res);
      } catch (e: any) {
        setError(e.message || "Failed to scan");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [domain]);

  const handleRescan = async () => {
    if (!domain) return;
    setLoading(true);
    setError(null);
    try {
      const res = await api.lookup(domain);
      setResult(res);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (url: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.lookup(url);
      setResult(res);
      window.history.replaceState(null, "", `/site/${res.domain}`);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-4">
        <SearchBar onSearch={handleSearch} loading={loading} />
      </div>

      {error && (
        <div className="mb-4 text-red-600 bg-red-50 border border-red-200 rounded-lg p-3 text-sm">
          {error}
        </div>
      )}

      {loading && !result && (
        <div className="text-center py-12 text-slate-500">
          Scanning {domain}...
        </div>
      )}

      {result && <ResultsPanel result={result} onRescan={handleRescan} />}
    </div>
  );
}
