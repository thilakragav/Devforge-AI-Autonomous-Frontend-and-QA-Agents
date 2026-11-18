import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number;
  subtext?: string;
  badge?: string;
  badgeColor?: 'emerald' | 'rose' | 'amber' | 'blue';
  icon?: React.ReactNode;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  label,
  value,
  subtext,
  badge,
  badgeColor = 'blue',
  icon
}) => {
  const badgeClasses = {
    emerald: 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
    rose: 'bg-rose-500/15 text-rose-400 border-rose-500/30',
    amber: 'bg-amber-500/15 text-amber-400 border-amber-500/30',
    blue: 'bg-blue-500/15 text-blue-400 border-blue-500/30',
  }[badgeColor];

  return (
    <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-sm hover:border-slate-600 transition duration-200">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {label}
        </span>
        {badge && (
          <span className={`text-[11px] font-mono font-bold px-2 py-0.5 rounded border ${badgeClasses}`}>
            {badge}
          </span>
        )}
      </div>

      <div className="flex items-baseline justify-between">
        <div className="text-3xl font-heading font-extrabold text-white tracking-tight">
          {value}
        </div>
        {icon && <div className="text-slate-400">{icon}</div>}
      </div>

      {subtext && (
        <div className="text-xs text-slate-400 mt-2 font-medium">
          {subtext}
        </div>
      )}
    </div>
  );
};
