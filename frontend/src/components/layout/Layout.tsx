import { Outlet } from "react-router-dom";
import { Header } from "./Header";

export function Layout() {
  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  );
}
