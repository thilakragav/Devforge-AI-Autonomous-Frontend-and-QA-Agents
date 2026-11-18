import React, { useState } from 'react';
import { Columns, SplitSquareVertical, Eye } from 'lucide-react';

interface Props {
  referenceImage: string;
  generatedImage: string;
  diffImage?: string;
  ssimScore?: number;
  pixelDiffPct?: number;
}

export const ImageCompareSlider: React.FC<Props> = ({
  referenceImage,
  generatedImage,
  diffImage,
  ssimScore,
  pixelDiffPct,
}) => {
  const [viewMode, setViewMode] = useState<'sideBySide' | 'slider' | 'diff'>('sideBySide');
  const [sliderPos, setSliderPos] = useState(50);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      {/* Controls Header */}
      <div className="p-4 bg-slate-950 border-b border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Visual Inspection Mode:
          </span>
          <div className="inline-flex rounded-lg bg-slate-900 p-0.5 border border-slate-800 text-xs">
            <button
              onClick={() => setViewMode('sideBySide')}
              className={`px-3 py-1 rounded-md flex items-center space-x-1.5 transition ${
                viewMode === 'sideBySide'
                  ? 'bg-amber-500/20 text-amber-400 font-semibold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Columns className="w-3.5 h-3.5" />
              <span>Side-by-Side</span>
            </button>
            <button
              onClick={() => setViewMode('slider')}
              className={`px-3 py-1 rounded-md flex items-center space-x-1.5 transition ${
                viewMode === 'slider'
                  ? 'bg-amber-500/20 text-amber-400 font-semibold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <SplitSquareVertical className="w-3.5 h-3.5" />
              <span>Split Slider</span>
            </button>
            {diffImage && (
              <button
                onClick={() => setViewMode('diff')}
                className={`px-3 py-1 rounded-md flex items-center space-x-1.5 transition ${
                  viewMode === 'diff'
                    ? 'bg-rose-500/20 text-rose-400 font-semibold'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                <Eye className="w-3.5 h-3.5" />
                <span>OpenCV Heatmap</span>
              </button>
            )}
          </div>
        </div>

        {ssimScore !== undefined && (
          <div className="flex items-center space-x-4 text-xs font-mono">
            <span className="text-slate-400">
              SSIM Score:{' '}
              <strong className="text-amber-400 font-bold">{ssimScore.toFixed(4)}</strong>
            </span>
            {pixelDiffPct !== undefined && (
              <span className="text-slate-400">
                Discrepancy:{' '}
                <strong className="text-slate-200">{pixelDiffPct.toFixed(2)}%</strong>
              </span>
            )}
          </div>
        )}
      </div>

      {/* Comparison Display Canvas */}
      <div className="p-6 bg-slate-950/60 flex items-center justify-center min-h-[440px]">
        {/* 1. Side-by-Side View */}
        {viewMode === 'sideBySide' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl">
            <div className="space-y-2">
              <div className="text-xs font-semibold text-slate-400 flex items-center justify-between">
                <span>Original Reference (RDGCC.com)</span>
                <span className="font-mono text-[10px] text-slate-500">1440 x 900</span>
              </div>
              <div className="rounded-lg overflow-hidden border border-slate-700 bg-slate-900 shadow">
                <img
                  src={referenceImage}
                  alt="Original Reference"
                  className="w-full h-auto object-cover"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="text-xs font-semibold text-slate-400 flex items-center justify-between">
                <span>Generated Astro Website (Rendered)</span>
                <span className="font-mono text-[10px] text-emerald-400">Active Build</span>
              </div>
              <div className="rounded-lg overflow-hidden border border-slate-700 bg-slate-900 shadow">
                <img
                  src={generatedImage}
                  alt="Generated Website Screenshot"
                  className="w-full h-auto object-cover"
                />
              </div>
            </div>
          </div>
        )}

        {/* 2. Interactive Split Slider View */}
        {viewMode === 'slider' && (
          <div className="relative w-full max-w-4xl h-[480px] rounded-lg overflow-hidden border border-slate-700 select-none shadow-2xl">
            {/* Generated Image Base */}
            <img
              src={generatedImage}
              alt="Generated Website"
              className="absolute inset-0 w-full h-full object-cover"
            />

            {/* Reference Image Overlay (Clipped) */}
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ width: `${sliderPos}%` }}
            >
              <img
                src={referenceImage}
                alt="Original Reference"
                className="absolute inset-0 w-full h-full object-cover max-w-none"
                style={{ width: '100%', height: '100%' }}
              />
            </div>

            {/* Slider Divider Bar */}
            <div
              className="absolute top-0 bottom-0 w-1 bg-amber-400 shadow-lg cursor-ew-resize flex items-center justify-center"
              style={{ left: `${sliderPos}%` }}
            >
              <div className="w-7 h-7 rounded-full bg-slate-900 border-2 border-amber-400 flex items-center justify-center text-[10px] font-bold text-amber-400 shadow-md">
                ↔
              </div>
            </div>

            {/* Range Input Trigger */}
            <input
              type="range"
              min="0"
              max="100"
              value={sliderPos}
              onChange={(e) => setSliderPos(Number(e.target.value))}
              className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-20"
            />

            {/* Corner Labels */}
            <span className="absolute bottom-3 left-3 px-2 py-1 rounded bg-slate-900/80 text-[10px] font-bold text-slate-300 pointer-events-none">
              Reference
            </span>
            <span className="absolute bottom-3 right-3 px-2 py-1 rounded bg-slate-900/80 text-[10px] font-bold text-emerald-400 pointer-events-none">
              Generated Astro
            </span>
          </div>
        )}

        {/* 3. OpenCV Contour Diff Overlay */}
        {viewMode === 'diff' && diffImage && (
          <div className="max-w-4xl w-full space-y-2">
            <div className="text-xs font-semibold text-slate-400 flex items-center justify-between">
              <span>OpenCV Discrepancy Heatmap & Bounding Boxes</span>
              <span className="text-xs font-mono text-rose-400">Red Zones Indicate Deviations</span>
            </div>
            <div className="rounded-lg overflow-hidden border border-rose-500/30 bg-slate-900 shadow-xl">
              <img
                src={diffImage}
                alt="OpenCV Visual Difference Overlay"
                className="w-full h-auto object-cover"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
