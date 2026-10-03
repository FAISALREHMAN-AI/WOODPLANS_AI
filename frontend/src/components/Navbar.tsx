import React from 'react';
import { Hammer, Sparkles, Plus, FileText, Layers, ShieldCheck } from 'lucide-react';

interface NavbarProps {
  currentView: string;
  onNavigate: (view: string) => void;
  onNewProject: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentView, onNavigate, onNewProject }) => {
  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between">
      <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate('new_project')}>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-600 to-amber-800 flex items-center justify-center shadow-lg shadow-amber-900/20 border border-amber-500/30">
          <Hammer className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="font-mono font-bold tracking-tight text-lg text-white">WOODPLAN<span className="text-amber-500">.AI</span></span>
            <span className="px-2 py-0.5 text-[10px] font-mono font-bold rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20">CAD V1.0</span>
          </div>
          <p className="text-xs text-slate-400 hidden sm:block">From Reference to Ready-to-Build</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-xs text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Dimension Inference Active</span>
        </div>

        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-amber-600 to-amber-700 hover:from-amber-500 hover:to-amber-600 text-white font-medium text-sm transition-all shadow-md shadow-amber-950/40 border border-amber-500/30 active:scale-95"
        >
          <Plus className="w-4 h-4" />
          <span>New Project</span>
        </button>
      </div>
    </header>
  );
};
