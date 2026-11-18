import React from 'react';
import { Play, RotateCw, ExternalLink, Sparkles } from 'lucide-react';
import { StatusBadge } from '../common/StatusBadge';

interface Props {
  title: string;
  subtitle: string;
  currentRunStatus?: string;
  iteration?: number;
  onTriggerRun?: () => void;
  onRefresh?: () => void;
  isLoading?: boolean;
}

export const Header: React.FC<Props> = ({
  title,
  subtitle,
  currentRunStatus = 'IDLE',
  iteration = 1,
  onTriggerRun,
  onRefresh,
  isLoading = false,
}) => {
  return (
    <header className="h-16 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80 px-8 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      <div className="flex items-center space-x-3">
        <div>
          <h1 className="text-base font-heading font-bold text-white tracking-tight flex items-center space-x-2">
            <span>{title}</span>
            {iteration > 0 && (
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400">
                v{iteration}
              </span>
            )}
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            {subtitle}
          </p>
        </div>
      </div>

      <div className="flex items-center space-x-3 sm:space-x-4">
        <div className="hidden sm:flex items-center space-x-2 text-xs bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-lg">
          <span className="text-slate-400 font-medium">Orchestrator:</span>
          <StatusBadge status={currentRunStatus} size="sm" />
        </div>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition"
          title="Refresh Workspace"
        >
          <RotateCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-amber-400' : ''}`} />
        </button>

        <a
          href="/api/preview/project_001"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-amber-400 hover:border-amber-500/30 transition shadow-sm"
        >
          <span>Live Site</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>

        {onTriggerRun && (
          <button
            onClick={onTriggerRun}
            disabled={isLoading}
            className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-extrabold text-xs shadow-md shadow-amber-500/20 transition disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{isLoading ? 'Running...' : 'Run Pipeline'}</span>
          </button>
        )}
      </div>
    </header>
  );
};
