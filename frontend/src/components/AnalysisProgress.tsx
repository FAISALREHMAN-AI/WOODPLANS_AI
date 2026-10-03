import React from 'react';
import { 
  CheckCircle2, 
  Circle, 
  Loader2, 
  Eye, 
  Ruler, 
  Scissors, 
  FileSpreadsheet, 
  Compass, 
  FileDown, 
  Layers 
} from 'lucide-react';

interface AnalysisProgressProps {
  currentStep: string;
  percentage: number;
}

const STAGES = [
  { label: 'Uploading Reference', threshold: 10, icon: Layers },
  { label: 'Detecting Product & Materials', threshold: 25, icon: Eye },
  { label: 'Analyzing Components & Geometry', threshold: 45, icon: Compass },
  { label: 'Estimating Dimensions & Scale Anchor', threshold: 60, icon: Ruler },
  { label: 'Building Cut List & Joinery Sequence', threshold: 75, icon: Scissors },
  { label: 'Generating Build Instructions', threshold: 85, icon: FileSpreadsheet },
  { label: 'Creating Technical Blueprint Diagrams', threshold: 92, icon: Compass },
  { label: 'Generating Printable Woodworking Plan PDF', threshold: 98, icon: FileDown },
];

export const AnalysisProgress: React.FC<AnalysisProgressProps> = ({ currentStep, percentage }) => {
  return (
    <div className="max-w-2xl mx-auto p-8 rounded-2xl bg-slate-900 border border-slate-800 shadow-2xl space-y-6">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 text-xs font-mono">
          <Loader2 className="w-3.5 h-3.5 animate-spin" />
          <span>ANALYZING YOUR WOODWORKING PROJECT...</span>
        </div>
        <h3 className="text-xl font-bold text-white tracking-tight">
          Decomposing Structure & Engineering DIY Plan
        </h3>
        <p className="text-sm text-slate-400">
          Inspecting joinery methods, scale anchors, nominal timber sizes, and cut geometries.
        </p>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs font-mono text-slate-400">
          <span>{currentStep || 'Processing reference...'}</span>
          <span className="text-amber-400 font-bold">{percentage}%</span>
        </div>
        <div className="h-2.5 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800 p-0.5">
          <div
            className="h-full bg-gradient-to-r from-amber-500 via-amber-400 to-emerald-400 rounded-full transition-all duration-300 shadow-sm"
            style={{ width: `${Math.max(percentage, 5)}%` }}
          />
        </div>
      </div>

      {/* Step Sequence Checklist */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-2">
        {STAGES.map((st, idx) => {
          const isDone = percentage >= st.threshold;
          const isCurrent = percentage < st.threshold && (idx === 0 || percentage >= STAGES[idx - 1].threshold);
          const Icon = st.icon;

          return (
            <div
              key={idx}
              className={`flex items-center gap-3 p-3 rounded-xl border text-xs transition-all ${
                isDone
                  ? 'border-emerald-500/20 bg-emerald-500/5 text-slate-300'
                  : isCurrent
                  ? 'border-amber-500/40 bg-amber-500/10 text-amber-300 font-semibold shadow-inner'
                  : 'border-slate-800/60 bg-slate-950/40 text-slate-500'
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-amber-400 animate-spin shrink-0" />
              ) : (
                <Circle className="w-4 h-4 text-slate-700 shrink-0" />
              )}
              <span className="truncate">{st.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
