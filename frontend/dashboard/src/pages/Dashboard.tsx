import React from 'react';
import { 
  FolderGit2, 
  Cpu, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight, 
  ExternalLink,
  Layers,
  Sparkles
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
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-[#0A192F] to-slate-900 border border-slate-800 rounded-2xl p-8 relative overflow-hidden shadow-xl">
        <div className="max-w-2xl relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Autonomous Closed-Loop Engineering</span>
          </div>
          <h2 className="text-3xl font-heading font-extrabold text-white tracking-tight mb-3">
            Multi-Agent Frontend & Automated QA Cockpit
          </h2>
          <p className="text-slate-300 text-sm leading-relaxed mb-6">
            Agent 1 converts visual design references (RDGCC.com) into modular Astro components, 
            while Agent 2 validates visual, responsive, and functional health with OpenCV and Playwright.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => onNavigate('input')}
              className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition shadow flex items-center space-x-1.5"
            >
              <span>Upload Design Reference</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => onNavigate('agent1')}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs border border-slate-700 transition"
            >
              View Generated Code
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <MetricCard
          label="Target Design"
          value="RDGCC.com"
          subtext="GCC Regional Development Holding"
          badge="Verified"
          badgeColor="emerald"
          icon={<FolderGit2 className="w-5 h-5" />}
        />
        <MetricCard
          label="Agent 1 (Code Generator)"
          value="Ready"
          subtext="Modular Astro Synthesizer"
          badge="Astro 4.x"
          badgeColor="blue"
          icon={<Cpu className="w-5 h-5" />}
        />
        <MetricCard
          label="Agent 2 (QA Automation)"
          value={`${passRate}% Pass`}
          subtext={`${passedTests} passed of ${totalTests} test cases`}
          badge="Playwright + CV"
          badgeColor={passRate >= 80 ? 'emerald' : 'amber'}
          icon={<CheckCircle2 className="w-5 h-5" />}
        />
        <MetricCard
          label="Visual Fidelity (SSIM)"
          value={ssimScore.toFixed(3)}
          subtext="OpenCV Structural Similarity"
          badge="Benchmark >= 0.8"
          badgeColor={ssimScore >= 0.8 ? 'emerald' : 'amber'}
          icon={<AlertTriangle className="w-5 h-5" />}
        />
      </div>

      {/* Two Column Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Latest QA Executive Summary */}
        <div className="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm">
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
                className="bg-emerald-500 h-full rounded-full transition-all duration-500"
              ></div>
            </div>
          </div>

          {/* Quick Metrics Breakdown */}
          <div className="grid grid-cols-3 gap-3 mb-6">
            <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Passed</span>
              <span className="text-xl font-extrabold text-emerald-400">{passedTests}</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Failed</span>
              <span className="text-xl font-extrabold text-rose-400">{failedTests}</span>
            </div>
            <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase block">Critical</span>
              <span className="text-xl font-extrabold text-amber-400">
                {latestReport?.critical_issues_count || 0}
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-slate-800">
            <span className="text-xs text-slate-400">
              Iteration {latestReport?.iteration || 1} • {latestReport?.timestamp || 'Latest build'}
            </span>
            <button
              onClick={() => onNavigate('reports')}
              className="text-xs font-semibold text-amber-400 hover:text-amber-300 flex items-center space-x-1"
            >
              <span>Full Audit Report</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Workflow & Architecture Status */}
        <div className="lg:col-span-5 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="text-base font-heading font-bold text-white mb-1">
              Multi-Agent Orchestration Flow
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              17-step closed-loop feedback pipeline
            </p>

            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  1
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Design Ingestion</h4>
                  <p className="text-[11px] text-slate-400">PDF page extraction, PNG/JPG processing, and Figma parsing.</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-blue-500/20 text-blue-400 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  2
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Agent 1 Modular Generation</h4>
                  <p className="text-[11px] text-slate-400">Generates 11 modular components, Sanity schemas, and global CSS.</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  3
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Agent 2 Multi-Tier QA</h4>
                  <p className="text-[11px] text-slate-400">Playwright viewports (Desktop/Tablet/Mobile), OpenCV SSIM, and DOM tests.</p>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                  4
                </div>
                <div>
                  <h4 className="text-xs font-bold text-white">Autonomous Feedback Loop</h4>
                  <p className="text-[11px] text-slate-400">Translates failed tests into surgical patches up to 3 iterations.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-6 border-t border-slate-800 mt-6">
            <button
              onClick={() => onNavigate('activity')}
              className="w-full py-2 rounded-lg bg-slate-950 border border-slate-800 hover:border-slate-700 text-xs text-slate-300 font-semibold flex items-center justify-center space-x-2 transition"
            >
              <span>View Live Agent Telemetry & Logs</span>
              <ExternalLink className="w-3.5 h-3.5 text-slate-500" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
