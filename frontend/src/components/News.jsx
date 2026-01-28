import { useState } from "react";

export default function NewsPlag() {
  const [text, setText] = useState("");

  const handleScan = async () => {
    await fetch("/api/plagiarism/news", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
  };

  return (
    <>
      <textarea
        placeholder="Paste news article content here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full h-48 bg-slate-800 rounded-xl p-4 outline-none resize-none mb-4"
      />

      <button
        onClick={handleScan}
        className="w-full py-3 bg-sky-500 rounded-xl font-semibold hover:bg-sky-600"
      >
        Scan News Article
      </button>
    </>
  );
}
