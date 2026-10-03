import React from 'react';
import { 
  FolderPlus, 
  FolderGit2, 
  History, 
  FileSpreadsheet, 
  Settings as SettingsIcon, 
  Ruler, 
  Compass,
  Boxes,
  HelpCircle
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  projectCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onNavigate, projectCount }) => {
  const navItems = [
    { id: 'new_project', label: 'New Project', icon: FolderPlus, badge: 'CAD' },
    { id: 'my_projects', label: 'My Projects', icon: FolderGit2, count: projectCount },
    { id: 'recent_analyses', label: 'Recent Analyses', icon: History },
    { id: 'generated_plans', label: 'Generated Plans', icon: FileSpreadsheet },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/60 flex flex-col justify-between p-4 hidden md:flex shrink-0">
      <div className="space-y-6">
        <div>
          <p className="text-[11px] font-mono font-semibold uppercase tracking-wider text-slate-500 mb-2 px-3">
            Core Workspace
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentView === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-amber-600/15 text-amber-400 border border-amber-500/30 font-semibold'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-amber-500' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
                      {item.badge}
                    </span>
                  )}
                  {item.count !== undefined && item.count > 0 && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-mono">
                      {item.count}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* CAD Drafting Reference Widget */}
        <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-2.5">
          <div className="flex items-center gap-2 text-slate-300 text-xs font-semibold">
            <Compass className="w-4 h-4 text-sky-400" />
            <span>Nominal Lumber Guide</span>
          </div>
          <div className="text-[11px] font-mono text-slate-400 space-y-1">
            <div className="flex justify-between border-b border-slate-800 pb-1">
              <span>1x4 Board:</span>
              <span className="text-slate-200">0.75" × 3.5"</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-1">
              <span>2x4 Stud:</span>
              <span className="text-slate-200">1.5" × 3.5"</span>
            </div>
            <div className="flex justify-between border-b border-slate-800 pb-1">
              <span>2x6 Joist:</span>
              <span className="text-slate-200">1.5" × 5.5"</span>
            </div>
            <div className="flex justify-between">
              <span>4x4 Post:</span>
              <span className="text-slate-200">3.5" × 3.5"</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-slate-800/80 space-y-2">
        <div className="flex items-center justify-between text-xs text-slate-500">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Woodworking AI Engine
          </span>
          <span className="font-mono text-[10px]">v1.0</span>
        </div>
      </div>
    </aside>
  );
};
