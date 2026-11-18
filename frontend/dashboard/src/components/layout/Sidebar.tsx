import React from 'react';
import { 
  LayoutDashboard, 
  UploadCloud, 
  Code2, 
  FileCheck2, 
  ClipboardList, 
  Activity, 
  Sparkles,
  ShieldCheck,
  ExternalLink,
  BookOpen
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
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none shadow-2xl z-40">
      <div>
        {/* Brand Header */}
        <div className="h-16 flex items-center px-6 border-b border-slate-800 space-x-3 bg-slate-950/80 backdrop-blur-md">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-amber-500 via-amber-400 to-amber-600 flex items-center justify-center font-bold text-slate-950 shadow-lg shadow-amber-500/20">
            <Sparkles className="w-5 h-5 text-slate-950" />
          </div>
          <div>
            <div className="font-heading font-extrabold text-sm tracking-tight text-white flex items-center space-x-1.5">
              <span className="tracking-wider bg-gradient-to-r from-white via-slate-100 to-amber-200 bg-clip-text text-transparent">DEVFORGE</span>
              <span className="text-amber-400 text-[10px] font-bold px-1.5 py-0.5 rounded bg-amber-500/15 border border-amber-500/30 font-mono">AI</span>
            </div>
            <div className="text-[10px] uppercase font-mono tracking-widest text-slate-400 font-medium">
              Autonomous Frontend & QA
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
                    ? 'bg-amber-500/15 text-amber-400 border border-amber-500/40 font-semibold shadow-sm'
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
      <div className="p-4 border-t border-slate-800 space-y-3 bg-slate-950/60">
        <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800">
          <div className="flex items-center justify-between text-[11px] text-slate-300 mb-1">
            <span className="flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span className="font-semibold">Target Design</span>
            </span>
            <span className="font-mono text-amber-400 font-bold">RDGCC.com</span>
          </div>
          <div className="text-[10px] text-slate-400">
            Gulf Regional Development Holding
          </div>
        </div>

        <div className="flex items-center justify-between pt-1 px-1">
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1 text-[11px] text-slate-400 hover:text-amber-400 transition"
          >
            <BookOpen className="w-3 h-3" />
            <span>Swagger API</span>
          </a>

          <a
            href="/api/preview/project_001"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1 text-[11px] text-slate-400 hover:text-amber-400 transition"
          >
            <span>Live Site</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-500 px-1 font-mono pt-1 border-t border-slate-800/80">
          <span>Engine Status</span>
          <span className="inline-flex items-center text-emerald-400 font-semibold">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
            ONLINE
          </span>
        </div>
      </div>
    </aside>
  );
};
