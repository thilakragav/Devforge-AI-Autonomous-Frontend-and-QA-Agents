import React from 'react';
import { Play, RotateCw, ExternalLink, Download } from 'lucide-react';
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
    <header className="h-16 bg-slate-950/80 backdrop-blur-md border-b border-slate-800 px-8 flex items-center justify-between sticky top-0 z-30">
      <div>
        <h1 className="text-base font-heading font-bold text-white tracking-tight flex items-center space-x-2">
          <span>{title}</span>
          {iteration > 0 && (
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300">
              v{iteration}
            </span>
          )}
        </h1>
        <p className="text-xs text-slate-400 font-medium">
          {subtitle}
        </p>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-xs">
          <span className="text-slate-500 font-medium">Orchestrator:</span>
          <StatusBadge status={currentRunStatus} size="sm" />
        </div>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition"
          title="Refresh Data"
        >
          <RotateCw className={`w-4 h-4 ${isLoading ? 'animate-spin text-amber-400' : ''}`} />
        </button>

        <a
          href="/api/preview/project_001"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-white hover:border-slate-700 transition"
        >
          <span>Live Site</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>

        {onTriggerRun && (
          <button
            onClick={onTriggerRun}
            disabled={isLoading}
            className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs shadow transition disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{isLoading ? 'Running Pipeline...' : 'Start Execution'}</span>
          </button>
        )}
      </div>
    </header>
  );
};
