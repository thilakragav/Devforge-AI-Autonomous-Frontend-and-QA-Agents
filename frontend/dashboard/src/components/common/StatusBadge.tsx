import React from 'react';

interface Props {
  status: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<Props> = ({ status, size = 'md' }) => {
  const s = status.toUpperCase();
  let color = 'bg-slate-700 text-slate-300 border-slate-600';

  if (s === 'PASSED' || s === 'PASS' || s === 'COMPLETED' || s === 'ONLINE') {
    color = 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
  } else if (s === 'FAILED' || s === 'FAIL' || s === 'FAILED_NEEDS_CORRECTION' || s === 'CRITICAL') {
    color = 'bg-rose-500/15 text-rose-400 border-rose-500/30';
  } else if (s === 'HIGH' || s === 'WARNING' || s === 'REFACTORING') {
    color = 'bg-amber-500/15 text-amber-400 border-amber-500/30';
  } else if (s === 'MEDIUM' || s === 'ANALYZING' || s === 'GENERATING' || s === 'TESTING' || s === 'BUILDING') {
    color = 'bg-blue-500/15 text-blue-400 border-blue-500/30';
  } else if (s === 'LOW' || s === 'INFO') {
    color = 'bg-slate-600/20 text-slate-300 border-slate-600/40';
  }

  const px = size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-2.5 py-1 text-xs';

  return (
    <span className={`inline-flex items-center font-mono font-semibold rounded-md border ${px} ${color}`}>
      {status}
    </span>
  );
};
