import React from 'react';
import { 
  FolderGit2, 
  Cpu, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight, 
  ExternalLink,
  Layers,
  Sparkles,
  Play,
  FileText,
  Workflow,
  ShieldCheck,
  Zap,
  Code2
} from 'lucide-react';
import { MetricCard } from '../components/layout/MetricCard';
import { StatusBadge } from '../components/common/StatusBadge';
import { QAReport, OrchestratorRunState } from '../types';

interface Props {
  latestReport?: QAReport | null;
  latestRun?: OrchestratorRunState | null;
  onNavigate: (tab: string) => void;
  onTriggerRun: () => void;
}

export const Dashboard: React.FC<Props> = ({
  latestReport,
  latestRun,
  onNavigate,
  onTriggerRun
}) => {
  const totalTests = latestReport?.total_tests || 12;
  const passedTests = latestReport?.passed_tests || 10;
  const failedTests = latestReport?.failed_tests || 2;
  const passRate = Math.round((passedTests / totalTests) * 100);
  const ssimScore = latestReport?.visual_metrics?.ssim_score || 0.88;

  return (
    <div className="space-y-8 pb-12">
      {/* Welcome Hero Banner */}
      <div className="bg-gradient-to-r from-slate-950 via-[#0A192F] to-slate-950 border border-slate-800 rounded-3xl p-8 md:p-10 relative overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 -mt-12 -mr-12 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div className="absolute bottom-0 left-1/3 -mb-12 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="max-w-3xl relative z-10">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-400 text-xs font-semibold mb-5 shadow-sm">
            <Sparkles className="w-3.5 h-3.5" />
            <span className="font-mono tracking-wide">DEVFORGE AI • AUTONOMOUS CLOSED-LOOP PLATFORM</span>
          </div>

          <h2 className="text-3xl sm:text-4xl md:text-5xl font-heading font-extrabold text-white tracking-tight mb-4 leading-tight">
            Automated Frontend Development & <span className="bg-gradient-to-r from-amber-300 via-amber-400 to-amber-500 bg-clip-text text-transparent">QA Automation</span>
          </h2>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed mb-8 max-w-2xl font-normal">
            Dual collaborative AI agents transforming website reference designs (RDGCC.com) into production-grade modular Astro components, 
            validated through pixel-level OpenCV SSIM and headless Playwright functional testing with automated self-correction loops.
          </p>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={onTriggerRun}
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-xs transition duration-200 shadow-lg shadow-amber-500/20 flex items-center space-x-2"
            >
              <Play className="w-4 h-4 fill-current" />
              <span>Execute Orchestrator Pipeline</span>
            </button>
            <button
              onClick={() => onNavigate('input')}
              className="px-4 py-2.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-white font-semibold text-xs border border-slate-700/80 transition flex items-center space-x-2"
            >
              <span>Upload Design Reference</span>
              <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
            </button>
            <a
              href="/api/preview/project_001"
              target="_blank"
              rel="noreferrer"
              className="px-4 py-2.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-amber-300 font-semibold text-xs border border-amber-500/30 transition flex items-center space-x-1.5"
            >
              <span>Preview Live Portal</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          </div>
        </div>
      </div>

      {/* Interactive Pipeline Architecture Tracker */}
      <div className="bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md">
        <div className="flex items-center justify-between mb-5">
          <div className="flex items-center space-x-2">
            <Workflow className="w-4 h-4 text-amber-400" />
            <h3 className="text-sm font-heading font-bold text-white tracking-wide uppercase">
              Closed-Loop Agent Pipeline Flow
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-400">
            Active Cycle: <span className="text-amber-400 font-bold">Iteration {latestRun?.current_iteration || 1} of 3</span>
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-amber-400 uppercase">Stage 01</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            </div>
            <div className="font-bold text-xs text-white mb-1">Design Ingestion</div>
            <div className="text-[11px] text-slate-400">PDF extraction, PNG/JPG parsing, Figma URL ingestion</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-blue-400 uppercase">Stage 02</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            </div>
            <div className="font-bold text-xs text-white mb-1">Vision Analysis</div>
            <div className="text-[11px] text-slate-400">Extracts layout, palette, typography, hierarchy tokens</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-purple-400 uppercase">Stage 03</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
            </div>
            <div className="font-bold text-xs text-white mb-1">Agent 1 Code Gen</div>
            <div className="text-[11px] text-slate-400">11 Astro components, Sanity schemas, homepage.js data</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase">Stage 04</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div className="font-bold text-xs text-white mb-1">Agent 2 QA Suite</div>
            <div className="text-[11px] text-slate-400">OpenCV SSIM diff, Playwright DOM & 3-viewport checks</div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/90 border border-amber-500/30 bg-amber-500/5 flex flex-col justify-between">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold text-amber-400 uppercase">Stage 05</span>
              <span className="text-[10px] font-bold text-amber-400">Auto-Feedback</span>
            </div>
            <div className="font-bold text-xs text-amber-300 mb-1">Self-Correction Loop</div>
            <div className="text-[11px] text-slate-400">Pydantic directives trigger targeted Astro refactoring</div>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard
          label="Target Design"
          value="RDGCC.com"
          subtext="Gulf Regional Development Holding"
          badge="Verified"
          badgeColor="emerald"
          icon={<FolderGit2 className="w-5 h-5 text-amber-400" />}
        />
        <MetricCard
          label="Agent 1 (Code Generator)"
          value="11 Files"
          subtext="Modular Astro Synthesizer"
          badge="Sanity CMS Ready"
          badgeColor="blue"
          icon={<Cpu className="w-5 h-5 text-blue-400" />}
        />
        <MetricCard
          label="Agent 2 (QA Automation)"
          value={`${passRate}% Pass`}
          subtext={`${passedTests} passed of ${totalTests} test cases`}
          badge="Playwright + CV"
          badgeColor={passRate >= 80 ? 'emerald' : 'amber'}
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-400" />}
        />
        <MetricCard
          label="Visual Fidelity (SSIM)"
          value={ssimScore.toFixed(3)}
          subtext="OpenCV Structural Similarity"
          badge="Threshold >= 0.8"
          badgeColor={ssimScore >= 0.8 ? 'emerald' : 'amber'}
          icon={<AlertTriangle className="w-5 h-5 text-amber-400" />}
        />
      </div>

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Latest QA Executive Summary */}
        <div className="lg:col-span-7 bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-heading font-bold text-white">
                Latest QA Test Execution
              </h3>
              <p className="text-xs text-slate-400">
                Automated multi-tier verification results for RDGCC
              </p>
            </div>
            <StatusBadge status={latestReport?.overall_status || 'PASSED'} size="sm" />
          </div>

          {/* Progress Bar */}
          <div className="space-y-2 mb-6">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Test Suite Pass Rate</span>
              <span className="text-emerald-400 font-bold">{passRate}%</span>
            </div>
            <div className="h-2.5 w-full bg-slate-800 rounded-full overflow-hidden flex">
              <div
                style={{ width: `${passRate}%` }}
                className="bg-gradient-to-r from-emerald-500 to-emerald-400 h-full rounded-full transition-all duration-500 shadow-sm"
              ></div>
            </div>
          </div>

          {/* Quick Metrics Breakdown */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block tracking-wider">Passed</span>
              <span className="text-2xl font-extrabold text-emerald-400 font-heading">{passedTests}</span>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block tracking-wider">Failed</span>
              <span className="text-2xl font-extrabold text-rose-400 font-heading">{failedTests}</span>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block tracking-wider">Critical</span>
              <span className="text-2xl font-extrabold text-amber-400 font-heading">
                {latestReport?.critical_issues_count || 0}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <span className="text-xs text-slate-400">
              Iteration {latestReport?.iteration || 1} • {latestReport?.timestamp || 'Latest verification run'}
            </span>
            <button
              onClick={() => onNavigate('reports')}
              className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center space-x-1.5 transition"
            >
              <span>Full Audit Report</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Workflow & Quick Navigation */}
        <div className="lg:col-span-5 bg-slate-950/80 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-md flex flex-col justify-between">
          <div>
            <h3 className="text-base font-heading font-bold text-white mb-1">
              Quick Workspace Access
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Inspect modular components and QA evidence
            </p>

            <div className="space-y-3">
              <button
                onClick={() => onNavigate('agent1')}
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 text-left transition flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
                    <Code2 className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-amber-400 transition">Agent 1 Code Workspace</div>
                    <div className="text-[11px] text-slate-400">Inspect Astro components & Sanity schemas</div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-white transition" />
              </button>

              <button
                onClick={() => onNavigate('agent2')}
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 text-left transition flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                    <ShieldCheck className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-amber-400 transition">Agent 2 QA & Visual Diff</div>
                    <div className="text-[11px] text-slate-400">OpenCV image comparison & viewports</div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-white transition" />
              </button>

              <button
                onClick={() => onNavigate('reports')}
                className="w-full p-3.5 rounded-xl bg-slate-900 hover:bg-slate-850 border border-slate-800 text-left transition flex items-center justify-between group"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
                    <FileText className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-white group-hover:text-amber-400 transition">Download Executive Reports</div>
                    <div className="text-[11px] text-slate-400">Export downloadable HTML & PDF audits</div>
                  </div>
                </div>
                <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-white transition" />
              </button>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 text-xs text-slate-500 flex items-center justify-between mt-4">
            <span>PoC Verification Mode</span>
            <span className="font-mono text-emerald-400 font-semibold">Deterministic + LLM</span>
          </div>
        </div>
      </div>
    </div>
  );
};
