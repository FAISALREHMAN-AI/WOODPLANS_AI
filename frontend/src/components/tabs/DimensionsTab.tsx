import React from 'react';
import { Ruler, Anchor, ShieldCheck, AlertCircle, HelpCircle } from 'lucide-react';
import { Project } from '../../types';

interface DimensionsTabProps {
  project: Project;
  onOpenEdit: () => void;
}

export const DimensionsTab: React.FC<DimensionsTabProps> = ({ project, onOpenEdit }) => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Ruler className="w-5 h-5 text-amber-500" />
            <span>Dimensional Engineering & Scale Inference</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Breakdown of reference-confirmed, estimated, and user-provided measurements.
          </p>
        </div>
        <button
          onClick={onOpenEdit}
          className="px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs font-mono transition-colors shadow-sm"
        >
          Override Dimensions
        </button>
      </div>

      {/* Scale Anchor Details Card */}
      <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
          <Anchor className="w-4 h-4 text-sky-400" />
          <span>Active Scale Anchor: {project.scale_anchor_desc || 'Visual Proportions Engine'}</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Overall Width</span>
              <span className="font-mono text-amber-400 font-bold">{project.width_status}</span>
            </div>
            <p className="text-2xl font-mono font-bold text-white">{project.overall_width}"</p>
            <p className="text-[11px] text-slate-500 mt-1">Nominal finished width with joints</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Overall Depth</span>
              <span className="font-mono text-amber-400 font-bold">{project.depth_status}</span>
            </div>
            <p className="text-2xl font-mono font-bold text-white">{project.overall_depth}"</p>
            <p className="text-[11px] text-slate-500 mt-1">Cross-section depth footprint</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
              <span>Overall Height</span>
              <span className="font-mono text-amber-400 font-bold">{project.height_status}</span>
            </div>
            <p className="text-2xl font-mono font-bold text-white">{project.overall_height}"</p>
            <p className="text-[11px] text-slate-500 mt-1">Elevation from floor to top peak</p>
          </div>
        </div>

        {project.analysis?.scale_inference_log && (
          <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs font-mono text-slate-400 space-y-1">
            <span className="text-slate-300 font-bold block">Inference Log:</span>
            <p>{project.analysis.scale_inference_log}</p>
          </div>
        )}
      </div>

      {/* Confidence Legend */}
      <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
          <span className="font-mono text-slate-300">USER_PROVIDED:</span>
          <span className="text-slate-500">Entered by builder</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
          <span className="font-mono text-slate-300">ESTIMATED:</span>
          <span className="text-slate-500">Inferred from proportions</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
          <span className="font-mono text-slate-300">CONFIRMED:</span>
          <span className="text-slate-500">Derived from blueprint</span>
        </div>
      </div>
    </div>
  );
};
