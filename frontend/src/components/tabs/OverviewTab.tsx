import React from 'react';
import { 
  Info, 
  Ruler, 
  Layers, 
  Clock, 
  Award, 
  Trees, 
  AlertTriangle, 
  ShieldAlert,
  CheckCircle2
} from 'lucide-react';
import { Project } from '../../types';

interface OverviewTabProps {
  project: Project;
  onOpenEdit: () => void;
}

export const OverviewTab: React.FC<OverviewTabProps> = ({ project, onOpenEdit }) => {
  const analysis = project.analysis;

  return (
    <div className="space-y-6">
      {/* Critical Verification Warning Alert */}
      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-3.5">
        <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h4 className="text-sm font-bold text-amber-300">
              {project.scale_warning || 'AI ESTIMATE — VERIFY BEFORE CUTTING'}
            </h4>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">
              CONFIDENCE: {project.scale_confidence}
            </span>
          </div>
          <p className="text-xs text-amber-200/80 leading-relaxed">
            AI-generated woodworking plans are estimates when exact measurements are not explicitly recorded on the reference. Always dry-fit parts, square your frames, and confirm critical clearances before glue-up.
          </p>
        </div>
      </div>

      {/* Overview Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Award className="w-4 h-4 text-amber-400" />
            <span>SKILL LEVEL</span>
          </div>
          <p className="text-base font-bold text-white">{project.difficulty_level}</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Clock className="w-4 h-4 text-sky-400" />
            <span>EST. BUILD TIME</span>
          </div>
          <p className="text-base font-bold text-white">{project.estimated_build_time}</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Trees className="w-4 h-4 text-emerald-400" />
            <span>PRIMARY LUMBER</span>
          </div>
          <p className="text-base font-bold text-white truncate">{project.primary_wood_species}</p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
            <Layers className="w-4 h-4 text-purple-400" />
            <span>WASTE ALLOWANCE</span>
          </div>
          <p className="text-base font-bold text-white">{project.waste_percentage}% Included</p>
        </div>
      </div>

      {/* Structural Topology & Method */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
          <h4 className="text-sm font-mono font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Info className="w-4 h-4 text-amber-500" />
            <span>Product Description & Analysis</span>
          </h4>
          <p className="text-sm text-slate-300 leading-relaxed">
            {project.description || analysis?.product_summary || 'Detailed structural build plan generated from source reference.'}
          </p>

          {analysis?.detected_features && analysis.detected_features.length > 0 && (
            <div className="pt-2 border-t border-slate-800">
              <span className="text-xs text-slate-400 block mb-2 font-mono">Detected Key Structural Features:</span>
              <div className="flex flex-wrap gap-1.5">
                {analysis.detected_features.map((feat, idx) => (
                  <span key={idx} className="text-xs px-2.5 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                    {feat}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
          <h4 className="text-sm font-mono font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
            <Layers className="w-4 h-4 text-sky-400" />
            <span>Construction Method & Joinery</span>
          </h4>
          <p className="text-sm text-slate-300 leading-relaxed">
            {analysis?.construction_method || 'Standard pocket-hole joinery combined with mechanical face clamping and PVA wood glue.'}
          </p>

          {analysis?.symmetry_notes && (
            <div className="pt-2 border-t border-slate-800">
              <span className="text-xs text-slate-400 block mb-1 font-mono">Symmetry & Assembly Logic:</span>
              <p className="text-xs text-slate-400 italic">{analysis.symmetry_notes}</p>
            </div>
          )}
        </div>
      </div>

      {/* Dimensions Summary Box */}
      <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-mono font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
              <Ruler className="w-4 h-4 text-emerald-400" />
              <span>Overall Finished Envelope Dimensions</span>
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Outer bounding dimensions with confidence classification.
            </p>
          </div>
          <button
            onClick={onOpenEdit}
            className="text-xs font-mono text-amber-400 hover:text-amber-300 font-semibold px-3 py-1.5 rounded-lg border border-amber-500/30 hover:bg-amber-500/10 transition-colors"
          >
            Edit Dimensions
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <span className="text-xs font-mono text-slate-500 block">OVERALL WIDTH (X)</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl font-mono font-bold text-white">{project.overall_width}"</span>
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                project.width_status === 'USER_PROVIDED'
                  ? 'bg-blue-500/20 text-blue-400'
                  : 'bg-amber-500/20 text-amber-400'
              }`}>
                {project.width_status}
              </span>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <span className="text-xs font-mono text-slate-500 block">OVERALL DEPTH (Y)</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl font-mono font-bold text-white">{project.overall_depth}"</span>
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                project.depth_status === 'USER_PROVIDED'
                  ? 'bg-blue-500/20 text-blue-400'
                  : 'bg-amber-500/20 text-amber-400'
              }`}>
                {project.depth_status}
              </span>
            </div>
          </div>

          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80">
            <span className="text-xs font-mono text-slate-500 block">OVERALL HEIGHT (Z)</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl font-mono font-bold text-white">{project.overall_height}"</span>
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                project.height_status === 'USER_PROVIDED'
                  ? 'bg-blue-500/20 text-blue-400'
                  : 'bg-amber-500/20 text-amber-400'
              }`}>
                {project.height_status}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
