import React from 'react';
import { Wrench, CheckCircle, HelpCircle } from 'lucide-react';
import { HardwareItem } from '../../types';

interface HardwareTabProps {
  hardware: HardwareItem[];
}

export const HardwareTab: React.FC<HardwareTabProps> = ({ hardware }) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Wrench className="w-5 h-5 text-amber-500" />
            <span>Fasteners & Hardware Requirements ({hardware.length} Items)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Categorized by visual confirmation, engineering inference, and optional hardware.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {hardware.map((item, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-2.5 hover:border-slate-700 transition-colors flex flex-col justify-between"
          >
            <div className="space-y-1.5">
              <div className="flex items-start justify-between">
                <h4 className="text-sm font-bold text-white">{item.item_name}</h4>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${
                  item.status === 'REFERENCE_VISIBLE'
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 font-bold'
                    : item.status === 'REFERENCE_INFERRED'
                    ? 'bg-sky-500/10 text-sky-400 border-sky-500/20 font-medium'
                    : 'bg-purple-500/10 text-purple-400 border-purple-500/20'
                }`}>
                  {item.status}
                </span>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono text-amber-400">
                <span>Quantity: {item.quantity}</span>
                {item.size_spec && <span>• Spec: {item.size_spec}</span>}
              </div>
            </div>

            {item.purpose && (
              <p className="text-xs text-slate-400 pt-2 border-t border-slate-800">
                <span className="text-slate-300 font-semibold">Application: </span>
                {item.purpose}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
