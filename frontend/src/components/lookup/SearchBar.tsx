import { useState } from "react";

interface Props {
  onSearch: (url: string) => void;
  onInputChange?: () => void;
  loading?: boolean;
  size?: "large" | "normal";
}

export function SearchBar({ onSearch, onInputChange, loading, size = "normal" }: Props) {
  const [value, setValue] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
    onInputChange?.();
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.trim()) {
      onSearch(value.trim());
    }
  };

  const isLarge = size === "large";

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div
        className={`flex border border-slate-200 bg-white rounded-lg shadow-sm focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 ${
          isLarge ? "h-14" : "h-10"
        }`}
      >
        <input
          type="text"
          value={value}
          onChange={handleChange}
          placeholder="输入网址查看技术栈 — e.g. taobao.com"
          className={`flex-1 bg-transparent outline-none px-4 text-slate-800 placeholder:text-slate-400 ${
            isLarge ? "text-lg" : "text-sm"
          }`}
        />
        <button
          type="submit"
          disabled={loading || !value.trim()}
          className={`bg-[#2563EB] text-white font-medium rounded-r-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors ${
            isLarge ? "px-8 text-base" : "px-4 text-sm"
          }`}
        >
          {loading ? "Scanning..." : "Scan"}
        </button>
      </div>
    </form>
  );
}
