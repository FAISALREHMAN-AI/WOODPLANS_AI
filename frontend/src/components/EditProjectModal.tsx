import React, { useState } from 'react';
import { X, RefreshCw, Save, Ruler, Layers, AlertTriangle } from 'lucide-react';
import { Project } from '../types';

interface EditProjectModalProps {
  project: Project;
  isOpen: boolean;
  onClose: () => void;
  onSave: (updated: Partial<Project>) => Promise<void>;
  onReanalyze: (options: any) => Promise<void>;
}

export const EditProjectModal: React.FC<EditProjectModalProps> = ({
  project,
  isOpen,
  onClose,
  onSave,
  onReanalyze
}) => {
  const [name, setName] = useState(project.name);
  const [productType, setProductType] = useState(project.product_type || '');
  const [width, setWidth] = useState(project.overall_width?.toString() || '');
  const [depth, setDepth] = useState(project.overall_depth?.toString() || '');
  const [height, setHeight] = useState(project.overall_height?.toString() || '');
  const [woodSpecies, setWoodSpecies] = useState(project.primary_wood_species || '');
  const [wastePct, setWastePct] = useState(project.waste_percentage || 15);
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) return null;

  const handleSaveOnly = async () => {
    setIsSubmitting(true);
    try {
      await onSave({
        name,
        product_type: productType,
        overall_width: parseFloat(width) || project.overall_width,
        overall_depth: parseFloat(depth) || project.overall_depth,
        overall_height: parseFloat(height) || project.overall_height,
        primary_wood_species: woodSpecies,
        waste_percentage: wastePct
      });
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTriggerReanalyze = async () => {
    setIsSubmitting(true);
    try {
      await onReanalyze({
        custom_width: parseFloat(width) || undefined,
        custom_depth: parseFloat(depth) || undefined,
        custom_height: parseFloat(height) || undefined,
        wood_species: woodSpecies,
        waste_percentage: wastePct
      });
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="w-full max-w-xl rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950">
          <div className="flex items-center gap-2.5">
            <Ruler className="w-5 h-5 text-amber-500" />
            <h3 className="text-base font-bold text-white">Edit Dimensions & Project Parameters</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto flex-1">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">Project Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-amber-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Product Type</label>
              <input
                type="text"
                value={productType}
                onChange={(e) => setProductType(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-amber-500"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1">Primary Lumber Species</label>
              <input
                type="text"
                value={woodSpecies}
                onChange={(e) => setWoodSpecies(e.target.value)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-amber-500"
              />
            </div>
          </div>

          {/* Envelope Dimensions */}
          <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-400">
                Outer Envelope Dimensions (Inches)
              </span>
              <span className="text-[11px] font-mono text-amber-400">Tolerance ±1/16"</span>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-xs text-slate-400 block mb-1">Width (X)</label>
                <input
                  type="number"
                  step="0.25"
                  value={width}
                  onChange={(e) => setWidth(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 font-mono focus:border-amber-500"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Depth (Y)</label>
                <input
                  type="number"
                  step="0.25"
                  value={depth}
                  onChange={(e) => setDepth(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 font-mono focus:border-amber-500"
                />
              </div>
              <div>
                <label className="text-xs text-slate-400 block mb-1">Height (Z)</label>
                <input
                  type="number"
                  step="0.25"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 font-mono focus:border-amber-500"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1">
              Lumber Waste & Kerf Allowance (%)
            </label>
            <div className="flex items-center gap-3">
              <input
                type="range"
                min="5"
                max="30"
                step="1"
                value={wastePct}
                onChange={(e) => setWastePct(parseInt(e.target.value))}
                className="flex-1 accent-amber-500"
              />
              <span className="w-12 text-center text-sm font-mono font-bold text-amber-400 bg-slate-950 px-2 py-1 rounded border border-slate-800">
                {wastePct}%
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Standard woodworking waste is 15% to cover blade kerf, knots, and trim squaring.
            </p>
          </div>

          <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-start gap-2.5 text-xs text-amber-300">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong>Re-analyzing</strong> recalculates all dependent component cut lists, board footages, blueprints, and assembly instructions based on your modified outer envelope.
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950 flex items-center justify-between">
          <button
            type="button"
            onClick={handleSaveOnly}
            disabled={isSubmitting}
            className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium transition-colors"
          >
            <Save className="w-4 h-4" />
            <span>Save Details Only</span>
          </button>

          <button
            type="button"
            onClick={handleTriggerReanalyze}
            disabled={isSubmitting}
            className="flex items-center gap-2 px-5 py-2 rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm transition-all shadow-md shadow-amber-500/20 active:scale-95"
          >
            <RefreshCw className={`w-4 h-4 ${isSubmitting ? 'animate-spin' : ''}`} />
            <span>RE-ANALYZE & RECALCULATE</span>
          </button>
        </div>
      </div>
    </div>
  );
};
