export default function CaptionPage() {
    return (
      <div className="max-w-xl bg-slate-900 rounded-2xl p-6 shadow-xl">
        <h2 className="text-lg font-semibold mb-4">Image Captioning</h2>
  
        <div className="border-2 border-dashed border-slate-700 rounded-xl p-10 text-center mb-6">
          <div className="text-cyan-400 text-5xl mb-4">☁</div>
          <p className="text-slate-400 mb-4">
            Drag & Drop Image Here <br /> or Browse Files
          </p>
          <button className="px-5 py-2 bg-emerald-600 rounded-lg hover:bg-emerald-700">
            Browse Files
          </button>
        </div>
  
        <button className="w-full py-3 bg-cyan-600 rounded-xl font-semibold hover:bg-cyan-700">
          Generate Caption
        </button>
      </div>
    );
  }
  