import React, { useState } from 'react';
import { Upload, FileText, Image as ImageIcon, Link2, Sparkles, CheckCircle2, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

interface Props {
  onSuccess: (runId: string) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const DesignInput: React.FC<Props> = ({ onSuccess, isLoading, setIsLoading }) => {
  const [file, setFile] = useState<File | null>(null);
  const [figmaUrl, setFigmaUrl] = useState<string>('https://figma.com/design/rdgcc-corporate-portal');
  const [maxIterations, setMaxIterations] = useState<number>(3);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [uploadedPath, setUploadedPath] = useState<string>('uploads/rdgcc_reference.png');
  const [dragActive, setDragActive] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setUploadStatus('Processing design reference...');

    try {
      let activePath = uploadedPath;

      // If custom file uploaded, send via base64
      if (file) {
        setUploadStatus(`Uploading ${file.name}...`);
        const reader = new FileReader();
        const base64Promise = new Promise<string>((resolve) => {
          reader.onload = () => {
            const result = reader.result as string;
            const b64 = result.split(',')[1];
            resolve(b64);
          };
          reader.readAsDataURL(file);
        });
        const b64Data = await base64Promise;
        const uploadRes = await api.uploadBase64(file.name, b64Data);
        activePath = uploadRes.saved_path;
        setUploadedPath(activePath);
      }

      setUploadStatus('Triggering Autonomous Multi-Agent Orchestrator...');
      const runRes = await api.triggerOrchestrator(
        activePath,
        figmaUrl.trim() ? figmaUrl : undefined,
        maxIterations
      );

      setUploadStatus(`Run launched: ${runRes.run_id}`);
      onSuccess(runRes.run_id);
    } catch (err: any) {
      setUploadStatus(`Error: ${err.message || 'Execution failed'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h2 className="text-2xl font-heading font-extrabold text-white tracking-tight">
          Design Ingestion & Analysis Trigger
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Submit website design mockups (PNG, JPG, PDF, or Figma URL) to initialize Agent 1 & Agent 2.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Upload Zone */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-2xl p-10 text-center transition-all ${
            dragActive
              ? 'border-amber-400 bg-amber-500/5'
              : 'border-slate-700/80 bg-slate-900/60 hover:border-slate-600'
          }`}
        >
          <div className="max-w-md mx-auto space-y-4">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center text-amber-400 shadow">
              <Upload className="w-6 h-6" />
            </div>

            <div>
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-sm font-bold text-amber-400 hover:text-amber-300">
                  Upload screenshot or PDF
                </span>
                <span className="text-sm text-slate-400"> or drag and drop</span>
                <input
                  id="file-upload"
                  type="file"
                  accept=".png,.jpg,.jpeg,.pdf,.webp"
                  onChange={handleFileChange}
                  className="sr-only"
                />
              </label>
              <p className="text-xs text-slate-500 mt-1">
                Supported formats: PNG, JPG, JPEG, PDF (multi-page rasterization enabled)
              </p>
            </div>

            {file ? (
              <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-xs text-slate-200">
                <FileText className="w-4 h-4 text-amber-400" />
                <span className="font-semibold">{file.name}</span>
                <span className="text-slate-400">({(file.size / 1024).toFixed(1)} KB)</span>
              </div>
            ) : (
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-800/60 border border-slate-700/50 text-[11px] text-slate-400">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Default reference pre-loaded: <strong>RDGCC.com Corporate Portal</strong></span>
              </div>
            )}
          </div>
        </div>

        {/* Alternative: Figma URL */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4 shadow-sm">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300">
            Figma Design URL (Optional)
          </label>
          <div className="relative">
            <Link2 className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
            <input
              type="url"
              value={figmaUrl}
              onChange={(e) => setFigmaUrl(e.target.value)}
              placeholder="https://www.figma.com/design/..."
              className="w-full bg-slate-950 border border-slate-700 rounded-lg pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 font-mono transition"
            />
          </div>
          <p className="text-[11px] text-slate-500">
            Agent 1 extracts design frames, color palettes, and component metadata directly from Figma specs.
          </p>
        </div>

        {/* Execution Settings */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 grid grid-cols-1 md:grid-cols-2 gap-6 shadow-sm">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Maximum Feedback Iterations
            </label>
            <select
              value={maxIterations}
              onChange={(e) => setMaxIterations(Number(e.target.value))}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3.5 py-2.5 text-xs text-white focus:outline-none focus:border-amber-400 transition"
            >
              <option value={1}>1 Iteration (Initial Synthesis Only)</option>
              <option value={2}>2 Iterations (1 Self-Correction Loop)</option>
              <option value={3}>3 Iterations (Full 3-Tier Quality Assurance)</option>
            </select>
            <p className="text-[11px] text-slate-500 mt-1">
              Limits automatic refactoring loops between Agent 1 and Agent 2.
            </p>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Execution Paradigm
            </label>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 flex items-center justify-between">
              <span className="flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                <span>Deterministic Reference Benchmark</span>
              </span>
              <span className="text-[10px] font-mono text-slate-500">No cloud credits required</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Verifies authentic OpenCV SSIM, Playwright viewports, and ReportLab PDF.
            </p>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex items-center justify-between pt-2">
          <div className="text-xs text-slate-400 font-mono">
            {uploadStatus}
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="px-6 py-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow-lg transition flex items-center space-x-2 disabled:opacity-50 cursor-pointer"
          >
            <Sparkles className="w-4 h-4 fill-current" />
            <span>{isLoading ? 'Processing Multi-Agent Pipeline...' : 'Start Analysis & Generation'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};
