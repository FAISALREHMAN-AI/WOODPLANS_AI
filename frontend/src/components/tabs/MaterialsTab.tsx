import React, { useState } from 'react';
import { Layers, ShoppingCart, Percent, AlertCircle } from 'lucide-react';
import { MaterialItem } from '../../types';

interface MaterialsTabProps {
  materials: MaterialItem[];
  wastePercentage: number;
  onUpdateWaste: (pct: number) => void;
}

export const MaterialsTab: React.FC<MaterialsTabProps> = ({ materials, wastePercentage, onUpdateWaste }) => {
  const [waste, setWaste] = useState<number>(wastePercentage || 15);

  const handleWasteChange = (newVal: number) => {
    setWaste(newVal);
    onUpdateWaste(newVal);
  };

  const totalBoards = materials.reduce((acc, m) => acc + m.calculated_boards, 0);

  return (
    <div className="space-y-6">
      {/* Waste Percentage Control Bar */}
      <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Percent className="w-4 h-4 text-amber-500" />
            <h4 className="text-sm font-bold text-white">Lumber Waste & Defect Calculation</h4>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Default 15% allowance covers blade kerf loss, end trimming, and natural wood defects.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <input
            type="range"
            min="5"
            max="30"
            step="1"
            value={waste}
            onChange={(e) => handleWasteChange(parseInt(e.target.value))}
            className="w-32 sm:w-48 accent-amber-500"
          />
          <span className="w-14 text-center font-mono font-bold text-xs text-amber-400 bg-slate-950 px-2 py-1 rounded border border-slate-800">
            {waste}%
          </span>
        </div>
      </div>

      {/* Materials Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/90 overflow-hidden shadow-xl">
        <div className="px-5 py-4 border-b border-slate-800 bg-slate-950 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShoppingCart className="w-4 h-4 text-emerald-400" />
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-300">
              Shopping List ({totalBoards} Total Standard Boards / Sheets)
            </span>
          </div>
          <span className="text-[11px] font-mono text-slate-500">Based on 8-foot (96") stock</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Lumber Category</th>
                <th className="py-3 px-4">Specification & Description</th>
                <th className="py-3 px-4 text-right">Required Linear Length</th>
                <th className="py-3 px-4 text-center">8-Foot Boards</th>
                <th className="py-3 px-4">Cutting / Selection Guidance</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {materials.map((m, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-amber-400">
                    {m.category}
                  </td>
                  <td className="py-3.5 px-4 font-sans text-white">
                    {m.description}
                  </td>
                  <td className="py-3.5 px-4 text-right text-sky-400 font-bold">
                    {m.required_board_length.toFixed(1)}" ({ (m.required_board_length / 12).toFixed(1)} ft)
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className="inline-block px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20 text-xs">
                      {m.calculated_boards} {m.category.toLowerCase().includes('plywood') ? 'sheet' : 'boards'}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-slate-400 font-sans text-xs">
                    {m.notes || 'Sight down board edge to verify straightness'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-2 font-mono">
        <AlertCircle className="w-4 h-4 text-amber-500 shrink-0" />
        <span>Approximate material calculation — verify against final cuts and available lumber yard lengths.</span>
      </div>
    </div>
  );
};
