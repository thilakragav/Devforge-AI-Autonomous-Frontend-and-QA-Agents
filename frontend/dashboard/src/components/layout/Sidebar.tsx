import React from 'react';
import { 
  LayoutDashboard, 
  UploadCloud, 
  Code2, 
  FileCheck2, 
  ClipboardList, 
  Activity, 
  Sparkles,
  ShieldCheck
} from 'lucide-react';

interface Props {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  systemMode?: string;
}

export const Sidebar: React.FC<Props> = ({ activeTab, setActiveTab, systemMode }) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'input', label: 'Design Input', icon: UploadCloud },
    { id: 'agent1', label: 'Agent 1 Workspace', icon: Code2 },
    { id: 'agent2', label: 'Agent 2 Workspace', icon: FileCheck2 },
    { id: 'reports', label: 'QA Reports', icon: ClipboardList },
    { id: 'activity', label: 'Agent Activity', icon: Activity },
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 border-b border-slate-800 space-x-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-amber-500 to-amber-600 flex items-center justify-center font-bold text-slate-950 shadow-md">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="font-heading font-extrabold text-sm tracking-tight text-white flex items-center space-x-1">
              <span>ANTIGRAVITY</span>
              <span className="text-amber-400">AI</span>
            </div>
            <div className="text-[10px] uppercase font-mono tracking-widest text-slate-500">
              Dev & QA Orchestrator
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1">
          <div className="px-3 pt-3 pb-1 text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Agents & Pipeline
          </div>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-xs font-medium transition duration-150 ${
                  isActive
                    ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900 border border-transparent'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-amber-400' : 'text-slate-500'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info & System Mode Badge */}
      <div className="p-4 border-t border-slate-800 space-y-3">
        <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between text-[11px] text-slate-400 mb-1">
            <span className="flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Target Design</span>
            </span>
            <span className="font-mono text-emerald-400 font-bold">RDGCC.com</span>
          </div>
          <div className="text-[10px] text-slate-500">
            Gulf Regional Development Holding
          </div>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 font-mono">
          <span>Engine Status</span>
          <span className="inline-flex items-center text-emerald-400">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
            ACTIVE
          </span>
        </div>
      </div>
    </aside>
  );
};
