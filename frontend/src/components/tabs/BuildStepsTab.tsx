import React from 'react';
import { 
  FileSpreadsheet, 
  CheckCircle2, 
  AlertTriangle, 
  Wrench, 
  Scissors, 
  Layers, 
  ShieldCheck,
  Ruler
} from 'lucide-react';
import { InstructionStep } from '../../types';

interface BuildStepsTabProps {
  instructions: InstructionStep[];
}

export const BuildStepsTab: React.FC<BuildStepsTabProps> = ({ instructions }) => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-amber-500" />
            <span>Step-by-Step Build Instructions ({instructions.length} Stages)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Sequential workshop workflow with objectives, required tooling, checkpoints, and safety protocols.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {instructions.map((step, idx) => (
          <div
            key={idx}
            className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 shadow-md hover:border-slate-700 transition-colors"
          >
            {/* Step Header */}
            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-xl bg-amber-500 text-slate-950 font-mono font-black flex items-center justify-center text-sm shadow-md shadow-amber-500/20">
                  {step.step_number}
                </span>
                <h4 className="text-base font-bold text-white tracking-tight">
                  {step.title}
                </h4>
              </div>

              {step.parts_used && (
                <div className="flex items-center gap-1.5 text-xs font-mono text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
                  <Layers className="w-3.5 h-3.5" />
                  <span>Parts: {step.parts_used}</span>
                </div>
              )}
            </div>

            {/* Objective */}
            {step.objective && (
              <p className="text-sm text-slate-300 font-medium">
                <span className="text-amber-400 font-mono font-bold">Objective: </span>
                {step.objective}
              </p>
            )}

            {/* Tooling & Cuts Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
              {step.tools && (
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-start gap-2.5">
                  <Wrench className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-slate-500 block text-[10px]">REQUIRED TOOLS</span>
                    <span className="text-slate-200">{step.tools}</span>
                  </div>
                </div>
              )}

              {step.cuts && (
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-start gap-2.5">
                  <Scissors className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-slate-500 block text-[10px]">CUTS & MACHINING</span>
                    <span className="text-slate-200">{step.cuts}</span>
                  </div>
                </div>
              )}
            </div>

            {/* Assembly Instructions */}
            {step.assembly && (
              <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 text-sm text-slate-200 space-y-2">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400 block">
                  Assembly Procedure:
                </span>
                <p className="leading-relaxed whitespace-pre-line text-xs sm:text-sm text-slate-300">
                  {step.assembly}
                </p>
              </div>
            )}

            {/* Checkpoint & Safety Callouts */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
              {step.checkpoint && (
                <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-start gap-2.5 text-xs text-emerald-300">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="block font-mono text-[11px] uppercase tracking-wide">Quality Checkpoint:</strong>
                    <span>{step.checkpoint}</span>
                  </div>
                </div>
              )}

              {step.safety_note && (
                <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/20 flex items-start gap-2.5 text-xs text-red-300">
                  <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                  <div>
                    <strong className="block font-mono text-[11px] uppercase tracking-wide">Safety Note:</strong>
                    <span>{step.safety_note}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
