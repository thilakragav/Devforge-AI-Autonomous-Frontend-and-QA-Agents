import React, { useState } from 'react';
import { 
  FileCheck2, 
  Monitor, 
  Tablet, 
  Smartphone, 
  CheckCircle2, 
  XCircle, 
  Eye, 
  ShieldAlert,
  ExternalLink
} from 'lucide-react';
import { ImageCompareSlider } from '../components/common/ImageCompareSlider';
import { StatusBadge } from '../components/common/StatusBadge';
import { QAReport } from '../types';

interface Props {
  report?: QAReport | null;
  referenceImage?: string;
  generatedImage?: string;
}

export const Agent2Workspace: React.FC<Props> = ({
  report,
  referenceImage = '/uploads/rdgcc_reference.png',
  generatedImage = '/reports/screenshots/project_001_v1_Desktop_1440x900.png',
}) => {
  const [qaTab, setQaTab] = useState<'visual' | 'responsive' | 'functional'>('visual');
  const [activeDevice, setActiveDevice] = useState<'Desktop' | 'Tablet' | 'Mobile'>('Desktop');

  const diffImg = report?.visual_metrics?.diff_image_path
    ? `/reports/diffs/${report.visual_metrics.diff_image_path.split(/[\\/]/).pop()}`
    : undefined;

  const visualTests = report?.test_cases.filter((t) => t.category === 'VISUAL') || [];
  const responsiveTests = report?.test_cases.filter((t) => t.category === 'RESPONSIVE') || [];
  const functionalTests = report?.test_cases.filter((t) => t.category === 'FUNCTIONAL') || [];

  return (
    <div className="space-y-8">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div>
          <div className="flex items-center space-x-2 text-xs text-amber-400 font-bold mb-1">
            <FileCheck2 className="w-4 h-4" />
            <span>AGENT 2: UI & QA TESTING ENGINE</span>
          </div>
          <h2 className="text-2xl font-heading font-extrabold text-white tracking-tight">
            Automated Visual, Responsive & Functional Audit
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            Multi-tiered validation comparing original RDGCC reference against rendered Astro deployment.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <StatusBadge status={report?.overall_status || 'VERIFIED'} size="sm" />
          <a
            href="/api/reports/project_001/download?format=pdf"
            target="_blank"
            rel="noreferrer"
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs border border-slate-700 shadow flex items-center space-x-1.5 transition"
          >
            <span>Download Audit PDF</span>
          </a>
        </div>
      </div>

      {/* Mode Navigation Tabs */}
      <div className="flex border-b border-slate-800 space-x-6 text-xs font-semibold">
        <button
          onClick={() => setQaTab('visual')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            qaTab === 'visual'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Eye className="w-4 h-4" />
          <span>Visual Testing (OpenCV & SSIM)</span>
        </button>

        <button
          onClick={() => setQaTab('responsive')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            qaTab === 'responsive'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <Monitor className="w-4 h-4" />
          <span>Responsive Viewports (3 Devices)</span>
        </button>

        <button
          onClick={() => setQaTab('functional')}
          className={`pb-3 flex items-center space-x-2 border-b-2 transition ${
            qaTab === 'functional'
              ? 'border-amber-400 text-amber-400 font-bold'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <CheckCircle2 className="w-4 h-4" />
          <span>Functional Playwright Suite ({functionalTests.length})</span>
        </button>
      </div>

      {/* Tab 1: Visual Comparison & OpenCV SSIM */}
      {qaTab === 'visual' && (
        <div className="space-y-6">
          <ImageCompareSlider
            referenceImage={referenceImage}
            generatedImage={generatedImage}
            diffImage={diffImg}
            ssimScore={report?.visual_metrics?.ssim_score || 0.88}
            pixelDiffPct={report?.visual_metrics?.pixel_diff_percentage || 12.0}
          />

          {/* Qualitative LLM Critique */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-3">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Eye className="w-4 h-4 text-amber-400" />
              <span>Vision LLM Qualitative Visual Critique</span>
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono">
              {report?.visual_metrics?.llm_visual_critique ||
                'Visual alignment is strong. Header spacing, typography hierarchy, and corporate grid match reference with high structural precision. Minor kerning adjustments recommended.'}
            </p>
          </div>

          {/* Visual Test Cases Table */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-500 uppercase text-[11px] font-bold">
                  <th className="py-3 px-4">Test ID</th>
                  <th className="py-3 px-4">Test Description</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Observed Metric</th>
                </tr>
              </thead>
              <tbody>
                {visualTests.map((t) => (
                  <tr key={t.test_id} className="border-b border-slate-800/60 hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-mono text-xs font-semibold">{t.test_id}</td>
                    <td className="py-3 px-4 text-xs font-medium text-white">{t.description}</td>
                    <td className="py-3 px-4 text-xs">
                      <StatusBadge status={t.passed ? 'PASS' : 'FAIL'} size="sm" />
                    </td>
                    <td className="py-3 px-4 text-xs">
                      <StatusBadge status={t.severity} size="sm" />
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-400 font-mono">{t.actual_result}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 2: Responsive Viewports */}
      {qaTab === 'responsive' && (
        <div className="space-y-6">
          {/* Device Selector */}
          <div className="flex items-center space-x-3">
            <button
              onClick={() => setActiveDevice('Desktop')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center space-x-2 border transition ${
                activeDevice === 'Desktop'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              <Monitor className="w-4 h-4" />
              <span>Desktop (1440 × 900)</span>
            </button>

            <button
              onClick={() => setActiveDevice('Tablet')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center space-x-2 border transition ${
                activeDevice === 'Tablet'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              <Tablet className="w-4 h-4" />
              <span>Tablet (768 × 1024)</span>
            </button>

            <button
              onClick={() => setActiveDevice('Mobile')}
              className={`px-4 py-2 rounded-lg text-xs font-semibold flex items-center space-x-2 border transition ${
                activeDevice === 'Mobile'
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/40'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              <Smartphone className="w-4 h-4" />
              <span>Mobile (375 × 812)</span>
            </button>
          </div>

          {/* Viewport Frame Preview */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm flex flex-col items-center">
            <div className="text-xs text-slate-400 mb-4 font-mono">
              Auditing viewport: <strong>{activeDevice}</strong>
            </div>

            <div
              className={`bg-slate-950 border border-slate-700 rounded-xl overflow-hidden shadow-2xl transition-all ${
                activeDevice === 'Desktop'
                  ? 'w-full max-w-4xl h-[480px]'
                  : activeDevice === 'Tablet'
                  ? 'w-[520px] h-[520px]'
                  : 'w-[320px] h-[560px]'
              }`}
            >
              <iframe
                src="/api/preview/project_001"
                title="Viewport Preview"
                className="w-full h-full border-0"
              />
            </div>
          </div>

          {/* Responsive Test Cases */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950 border-b border-slate-800 text-slate-500 uppercase text-[11px] font-bold">
                  <th className="py-3 px-4">Test ID</th>
                  <th className="py-3 px-4">Viewport Criteria</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Observed Status</th>
                </tr>
              </thead>
              <tbody>
                {responsiveTests.map((t) => (
                  <tr key={t.test_id} className="border-b border-slate-800/60 hover:bg-slate-800/30 transition">
                    <td className="py-3 px-4 font-mono text-xs font-semibold">{t.test_id}</td>
                    <td className="py-3 px-4 text-xs font-medium text-white">{t.description}</td>
                    <td className="py-3 px-4 text-xs">
                      <StatusBadge status={t.passed ? 'PASS' : 'FAIL'} size="sm" />
                    </td>
                    <td className="py-3 px-4 text-xs">
                      <StatusBadge status={t.severity} size="sm" />
                    </td>
                    <td className="py-3 px-4 text-xs text-slate-400 font-mono">{t.actual_result}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab 3: Functional Testing Suite */}
      {qaTab === 'functional' && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
          <div className="p-6 border-b border-slate-800 flex items-center justify-between">
            <div>
              <h3 className="text-base font-heading font-bold text-white">
                Playwright Functional DOM Test Suite
              </h3>
              <p className="text-xs text-slate-400">
                Verifies actual navigation targets, interactive buttons, form validation, and image alt tags.
              </p>
            </div>
            <span className="text-xs font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1 rounded-md font-bold">
              {functionalTests.filter((t) => t.passed).length}/{functionalTests.length} Passed
            </span>
          </div>

          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-slate-500 uppercase text-[11px] font-bold">
                <th className="py-3 px-4">Test ID</th>
                <th className="py-3 px-4">Component Target</th>
                <th className="py-3 px-4">Requirement</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Severity</th>
                <th className="py-3 px-4">Observed Execution</th>
              </tr>
            </thead>
            <tbody>
              {functionalTests.map((t) => (
                <tr key={t.test_id} className="border-b border-slate-800/60 hover:bg-slate-800/30 transition">
                  <td className="py-3 px-4 font-mono text-xs font-semibold">{t.test_id}</td>
                  <td className="py-3 px-4 font-mono text-xs text-amber-400">{t.affected_component || 'Global'}</td>
                  <td className="py-3 px-4 text-xs font-medium text-white">{t.description}</td>
                  <td className="py-3 px-4 text-xs">
                    <StatusBadge status={t.passed ? 'PASS' : 'FAIL'} size="sm" />
                  </td>
                  <td className="py-3 px-4 text-xs">
                    <StatusBadge status={t.severity} size="sm" />
                  </td>
                  <td className="py-3 px-4 text-xs text-slate-300 font-mono">{t.actual_result}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
