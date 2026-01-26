import { useState } from "react";
import CaptionPage from "../components/Caption.jsx";
import PlagiarismPage from "../components/Plag.jsx";

export default function Home() {
  const [active, setActive] = useState("caption");

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#020617] via-[#020617] to-[#0f172a] text-white px-6 md:px-12 py-8">
      
      {/* Header */}
      <header className="mb-10 flex items-center justify-between">
        <div>
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight">
            GetChecked
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            AI-powered captioning & plagiarism detection
          </p>
        </div>
      </header>

      {/* Navigation */}
      <nav className="flex gap-8 mb-10 border-b border-slate-800">
        <button
          onClick={() => setActive("caption")}
          className={`relative pb-3 text-sm font-medium transition-colors ${
            active === "caption"
              ? "text-cyan-400"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Caption Generator
          {active === "caption" && (
            <span className="absolute left-0 -bottom-px h-[2px] w-full bg-cyan-400 rounded-full" />
          )}
        </button>

        <button
          onClick={() => setActive("plag")}
          className={`relative pb-3 text-sm font-medium transition-colors ${
            active === "plag"
              ? "text-cyan-400"
              : "text-slate-400 hover:text-white"
          }`}
        >
          Plagiarism Detection
          {active === "plag" && (
            <span className="absolute left-0 -bottom-px h-[2px] w-full bg-cyan-400 rounded-full" />
          )}
        </button>
      </nav>

      {/* Content Container */}
      <main className="max-w-7xl mx-auto">
        <div className="bg-slate-950/60 backdrop-blur-xl border border-slate-800 rounded-3xl p-6 md:p-10 shadow-2xl">
          {active === "caption" && <CaptionPage />}
          {active === "plag" && <PlagiarismPage />}
        </div>
      </main>
    </div>
  );
}
