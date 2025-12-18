import React, { useState, useCallback } from 'react';

interface AnalysisResult {
  label: string;
  confidence: number;
  gemini: {
    description: string;
    action: string;
  };
}

const analyzeImage = async (file: File): Promise<AnalysisResult> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to analyze image");
  }

  return response.json();
};

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.type.startsWith('image/')) {
      processFile(droppedFile);
    }
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = (selectedFile: File) => {
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    try {
      const data = await analyzeImage(file);
      setResult(data);
    } catch (err) {
      setError("Failed to analyze image. Ensure backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4 text-white">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[50%] -left-[50%] w-[200%] h-[200%] bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-purple-500/20 via-transparent to-transparent animate-spin-slow"></div>
      </div>

      <div className="relative bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl p-8 max-w-2xl w-full border border-white/20">
        <div className="text-center mb-10">
          <h1 className="text-5xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 drop-shadow-sm">
            AI Plastic Spotter
          </h1>
          <p className="text-lg text-blue-100/80 font-light tracking-wide">
            Identify trash & learn how to recycle it instantly.
          </p>
        </div>

        <div
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          className={`group relative border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-300 cursor-pointer overflow-hidden ${file
            ? 'border-green-400 bg-green-400/10'
            : 'border-white/30 hover:border-blue-400 hover:bg-white/5'
            }`}
        >
          <input
            type="file"
            id="fileInput"
            className="hidden"
            accept="image/*"
            onChange={handleFileChange}
          />

          {preview ? (
            <div className="relative z-10">
              <img
                src={preview}
                alt="Preview"
                className="max-h-80 mx-auto rounded-xl shadow-2xl ring-4 ring-white/10"
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                  setPreview(null);
                  setResult(null);
                }}
                className="absolute -top-4 -right-4 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition shadow-lg hover:scale-110"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
          ) : (
            <label htmlFor="fileInput" className="cursor-pointer block h-full z-10 relative">
              <div className="text-7xl mb-6 transform group-hover:scale-110 transition-transform duration-300">📸</div>
              <p className="text-2xl font-semibold text-white mb-2">
                Drag & Drop Image
              </p>
              <p className="text-sm text-blue-200">
                or click to browse files
              </p>
            </label>
          )}
        </div>

        {file && !result && (
          <div className="mt-8 text-center">
            <button
              onClick={handleSubmit}
              disabled={loading}
              className={`px-10 py-4 rounded-full font-bold text-lg text-white shadow-xl transition-all transform hover:scale-105 active:scale-95 ${loading
                ? 'bg-slate-600 cursor-not-allowed opacity-70'
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 hover:shadow-blue-500/30'
                }`}
            >
              {loading ? (
                <span className="flex items-center justify-center gap-3">
                  <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Identify Trash 🔍'
              )}
            </button>
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-500/20 text-red-200 rounded-xl text-center border border-red-500/50 backdrop-blur-sm">
            {error}
          </div>
        )}

        {result && (
          <div className="mt-10 animate-fade-in space-y-6">
            <div className="bg-slate-800/50 rounded-2xl p-6 border border-white/10">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-bold text-white tracking-tight">
                  {result.label}
                </h2>
                <span className="px-4 py-1.5 bg-green-500/20 text-green-300 rounded-full text-sm font-bold border border-green-500/30">
                  {(result.confidence * 100).toFixed(1)}% Match
                </span>
              </div>

              <div className="grid gap-4">
                <div className="p-5 bg-blue-900/30 rounded-xl border border-blue-500/30 hover:bg-blue-900/40 transition-colors">
                  <h3 className="font-bold text-blue-300 mb-2 flex items-center gap-2">
                    <span>💡</span> Did you know?
                  </h3>
                  <p className="text-blue-100 leading-relaxed max-h-40 overflow-y-auto custom-scrollbar">{result.gemini.description}</p>
                </div>

                <div className="p-5 bg-green-900/30 rounded-xl border border-green-500/30 hover:bg-green-900/40 transition-colors">
                  <h3 className="font-bold text-green-300 mb-2 flex items-center gap-2">
                    <span>♻️</span> Action Plan
                  </h3>
                  <p className="text-green-100 leading-relaxed max-h-40 overflow-y-auto custom-scrollbar">{result.gemini.action}</p>
                </div>
              </div>
            </div>

            <button
              onClick={() => {
                setFile(null);
                setPreview(null);
                setResult(null);
              }}
              className="w-full py-3 text-slate-400 hover:text-white font-medium transition-colors border-t border-white/10"
            >
              Analyze another item
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
