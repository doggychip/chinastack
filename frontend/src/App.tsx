import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";
import { SitesPage } from "./pages/SitesPage";
import { TechnologiesPage } from "./pages/TechnologiesPage";
import { TechDetailPage } from "./pages/TechDetailPage";
import { StatsPage } from "./pages/StatsPage";

function NotFoundPage() {
  return (
    <div className="text-center py-20">
      <h1 className="text-6xl font-bold text-slate-300 mb-4">404</h1>
      <p className="text-slate-500 mb-6">Page not found</p>
      <Link to="/" className="text-blue-600 hover:underline">
        Back to home
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/site/:domain" element={<ResultsPage />} />
          <Route path="/sites" element={<SitesPage />} />
          <Route path="/technologies" element={<TechnologiesPage />} />
          <Route path="/technologies/:slug" element={<TechDetailPage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
