import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";
import { SitesPage } from "./pages/SitesPage";
import { TechnologiesPage } from "./pages/TechnologiesPage";
import { TechDetailPage } from "./pages/TechDetailPage";
import { StatsPage } from "./pages/StatsPage";

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
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
