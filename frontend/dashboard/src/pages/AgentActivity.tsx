import React, { useState } from 'react';
import { 
  Activity, 
  RotateCw, 
  Filter, 
  Terminal, 
  Layers, 
  Clock, 
  CheckCircle2, 
  AlertCircle,
  Cpu
} from 'lucide-react';
import { StatusBadge } from '../components/common/StatusBadge';
import { RunStepLog, OrchestratorRunState } from '../types';

interface Props {
  logs: RunStepLog[];
  runState?: OrchestratorRunState | null;
  onRefresh?: () => void;
}

export const AgentActivity: React.FC<Props> = ({ logs, runState, onRefresh }) => {
  const [filterLevel, setFilterLevel] = useState<string>('ALL');

  const filteredLogs = filterLevel === 'ALL'
    ? logs
    : logs.filter((l) => l.level.toUpperCase() === filterLevel);

  return (
    <div className="space-y-8">
      {/* Workspace Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm">
        <div>
          <div className="flex items-center space-x-2 text-xs text-amber-400 font-bold mb-1">
            <Activity className="w-4 h-4" />
            <span>REAL-TIME AGENT TELEMETRY</span>
          </div>
          <h2 className="text-2xl font-heading font-extrabold text-white tracking-tight">
            Execution Ledger & Feedback History
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl leading-relaxed">
            Live event logs, inter-agent communication messages, and self-correction loop state.
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <StatusBadge status={runState?.status || 'IDLE'} size="sm" />
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
              title="Refresh Logs"
            >
              <RotateCw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Multi-Agent Stages Pipeline */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Current Processing Stage
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {[
            { stage: 'ANALYZING', label: '1. Vision Analysis', desc: 'Decompose Reference' },
            { stage: 'GENERATING', label: '2. Code Synthesis', desc: 'Modular Astro AST' },
            { stage: 'BUILDING', label: '3. Compilation', desc: 'Validate & Materialize' },
            { stage: 'TESTING', label: '4. QA Execution', desc: 'Playwright + OpenCV' },
            { stage: 'REFACTORING', label: '5. Self-Correction', desc: 'Targeted Fixes' },
            { stage: 'COMPLETED', label: '6. Verified Build', desc: 'Reports Ready' },
          ].map((s) => {
            const isCurrent = runState?.status === s.stage;
            const isDone = runState?.status === 'COMPLETED';
            return (
              <div
                key={s.stage}
                className={`p-3 rounded-lg border text-center transition ${
                  isCurrent
                    ? 'bg-amber-500/10 border-amber-500 text-amber-400 shadow-md font-bold'
                    : isDone
                    ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300'
                    : 'bg-slate-950 border-slate-800 text-slate-500'
                }`}
              >
                <div className="text-xs font-bold font-heading">{s.label}</div>
                <div className="text-[10px] text-slate-400 mt-1">{s.desc}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Feedback Iteration History */}
      {runState && runState.correction_history.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-sm space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center space-x-2">
            <RotateCw className="w-4 h-4" />
            <span>Autonomous Feedback Correction Loops ({runState.correction_history.length})</span>
          </h3>
          <div className="space-y-3">
            {runState.correction_history.map((dir, idx) => (
              <div key={idx} className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-white">
                    Iteration {dir.iteration} $\to$ {dir.iteration + 1}
                  </span>
                  <span className="font-mono text-amber-400 text-[11px]">
                    Target: {dir.target_components.join(', ')}
                  </span>
                </div>
                <ul className="text-xs text-slate-400 space-y-1 pl-4 list-disc">
                  {dir.actionable_instructions.map((inst, i) => (
                    <li key={i}>{inst}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Real-time Streaming Logs Console */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg flex flex-col h-[520px]">
        {/* Console Header Bar */}
        <div className="h-12 bg-slate-950 border-b border-slate-800 px-5 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Terminal className="w-4 h-4 text-amber-400" />
            <span className="text-xs font-mono font-bold text-white">
              System & Agent Event Log ({filteredLogs.length})
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded px-2.5 py-1 text-xs text-slate-300 font-mono focus:outline-none"
            >
              <option value="ALL">All Levels</option>
              <option value="INFO">Info</option>
              <option value="SUCCESS">Success</option>
              <option value="WARNING">Warning</option>
              <option value="ERROR">Error</option>
            </select>
          </div>
        </div>

        {/* Console Log Rows */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2 font-mono text-xs bg-[#050C1A]">
          {filteredLogs.length === 0 ? (
            <div className="text-slate-500 italic py-8 text-center">
              No logs registered yet. Trigger a run from Design Input to inspect activity.
            </div>
          ) : (
            filteredLogs.map((l, idx) => {
              let levelColor = 'text-slate-400';
              if (l.level === 'SUCCESS') levelColor = 'text-emerald-400 font-bold';
              else if (l.level === 'WARNING') levelColor = 'text-amber-400 font-bold';
              else if (l.level === 'ERROR') levelColor = 'text-rose-400 font-bold';

              return (
                <div key={idx} className="flex items-start space-x-3 py-1 border-b border-slate-900/60 hover:bg-slate-900/30">
                  <span className="text-slate-600 shrink-0 text-[11px]">
                    {l.timestamp.split('T')[1]?.slice(0, 8) || l.timestamp}
                  </span>
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-900 border border-slate-800 text-slate-300 shrink-0 font-semibold">
                    {l.agent}
                  </span>
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-slate-900/80 text-slate-400 shrink-0">
                    {l.stage}
                  </span>
                  <span className={`flex-1 break-all ${levelColor}`}>
                    {l.message}
                  </span>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
