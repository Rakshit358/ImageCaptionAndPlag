import { useRef, useState } from "react";
import ResearchPlag from "./Research";
import BlogPlag from "./Blog";
import NewsPlag from "./News";

export default function PlagiarismPage() {
  const [tab, setTab] = useState("Research");
  const fileInputRef = useRef(null);

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleSearch = () => {
    console.log("Detect plagiarism clicked");
    // add logic here
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      
      {/* Image Checking */}
      <div className="bg-slate-900 rounded-2xl p-6 shadow-xl text-white">
        <h2 className="text-lg font-semibold mb-4">Image Checking</h2>

        <div className="border-2 border-dashed border-slate-700 rounded-xl p-10 text-center">
          <div className="text-cyan-400 text-5xl mb-4">☁</div>

          <p className="text-slate-400 mb-4">
            Upload image for plagiarism check
          </p>

          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            className="hidden"
          />

          <button
            onClick={handleBrowseClick}
            className="px-5 py-2 bg-emerald-600 rounded-lg hover:bg-emerald-700"
          >
            Browse Files
          </button>
        </div>

        <button
          onClick={handleSearch}
          className="mt-4 px-5 py-2 bg-cyan-600 rounded-lg hover:bg-cyan-700"
        >
          Detect the Plag
        </button>
      </div>

      {/* Text Checking */}
      <div className="bg-slate-900 rounded-2xl p-6 shadow-xl text-white">
        <nav className="flex gap-3 mb-4">
          {["Research", "Blogs", "News"].map((item) => (
            <button
              key={item}
              onClick={() => setTab(item)}
              className={`px-4 py-2 rounded-full text-sm transition ${
                tab === item ? "bg-cyan-600" : "bg-slate-700 hover:bg-slate-600"
              }`}
            >
              {item}
            </button>
          ))}
        </nav>

        {tab === "Research" && <ResearchPlag />}
        {tab === "Blogs" && <BlogPlag />}
        {tab === "News" && <NewsPlag />}
      </div>
    </div>
  );
}
