import React from 'react';
import { Layers, Boxes, Tag, ShieldCheck } from 'lucide-react';
import { ComponentItem } from '../../types';

interface ComponentsTabProps {
  components: ComponentItem[];
}

export const ComponentsTab: React.FC<ComponentsTabProps> = ({ components }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Boxes className="w-5 h-5 text-amber-500" />
            <span>Component Decomposition ({components.length} Identified Parts)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Individual anatomical members, nominal lumber stock, cut types, and engineering purpose.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {components.map((comp, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-3">
                <span className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 border border-amber-500/30 font-mono font-bold flex items-center justify-center text-sm">
                  {comp.part_id}
                </span>
                <div>
                  <h4 className="text-sm font-bold text-white">{comp.part_name}</h4>
                  <span className="text-xs font-mono text-slate-400">Qty: {comp.quantity} pcs</span>
                </div>
              </div>

              <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${
                comp.confidence === 'HIGH'
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                  : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
              }`}>
                {comp.confidence} CONFIDENCE
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono bg-slate-950 p-3 rounded-xl border border-slate-800/80">
              <div>
                <span className="text-slate-500 block text-[10px]">NOMINAL STOCK</span>
                <span className="text-slate-200 font-bold">{comp.nominal_lumber_size} ({comp.material})</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">FINISHED CUT</span>
                <span className="text-amber-400 font-bold">
                  {comp.finished_length}" × {comp.finished_width}" × {comp.finished_thickness}"
                </span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">CUT TYPE / ANGLE</span>
                <span className="text-slate-300">{comp.cut_type} @ {comp.angles}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">JOINERY METHOD</span>
                <span className="text-slate-300">{comp.joinery}</span>
              </div>
            </div>

            {comp.purpose && (
              <p className="text-xs text-slate-400 italic">
                <strong className="text-slate-300 not-italic">Function: </strong>
                {comp.purpose}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
