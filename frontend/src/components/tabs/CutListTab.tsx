import React, { useState } from 'react';
import { Scissors, Download, Copy, Check, Filter } from 'lucide-react';
import { CutListItem } from '../../types';

interface CutListTabProps {
  cutList: CutListItem[];
  productName: string;
}

export const CutListTab: React.FC<CutListTabProps> = ({ cutList, productName }) => {
  const [copied, setCopied] = useState(false);
  const [filterMaterial, setFilterMaterial] = useState<string>('all');

  const materials = Array.from(new Set(cutList.map(c => c.lumber_size)));

  const filtered = filterMaterial === 'all'
    ? cutList
    : cutList.filter(c => c.lumber_size === filterMaterial);

  const copyToClipboard = () => {
    const text = [
      `MASTER CUT LIST — ${productName}`,
      `ID\tPART NAME\tQTY\tLUMBER\tLENGTH\tWIDTH\tTHICKNESS\tANGLE\tNOTES\tSTATUS`,
      ...cutList.map(c => `${c.part_id}\t${c.part_name}\t${c.quantity}\t${c.lumber_size}\t${c.length}"\t${c.width}"\t${c.thickness}"\t${c.angle}\t${c.notes || ''}\t${c.confidence}`)
    ].join('\n');

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const exportCSV = () => {
    const rows = [
      ['Part ID', 'Part Name', 'Qty', 'Lumber Size', 'Length (in)', 'Width (in)', 'Thickness (in)', 'Angle', 'Notes', 'Confidence'],
      ...cutList.map(c => [c.part_id, c.part_name, c.quantity.toString(), c.lumber_size, c.length.toString(), c.width.toString(), c.thickness.toString(), c.angle, c.notes || '', c.confidence])
    ];
    const csvContent = 'data:text/csv;charset=utf-8,' + rows.map(e => e.map(val => `"${val}"`).join(',')).join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `${productName.replace(/\s+/g, '_')}_cut_list.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Scissors className="w-5 h-5 text-amber-500" />
            <span>Master Cut List ({cutList.length} items)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Mill parts in order of length. Verify actual thickness of bought lumber prior to cutting joinery.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {materials.length > 1 && (
            <select
              value={filterMaterial}
              onChange={(e) => setFilterMaterial(e.target.value)}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 font-mono focus:border-amber-500"
            >
              <option value="all">All Lumber Sizes</option>
              {materials.map(m => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          )}

          <button
            onClick={copyToClipboard}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-mono text-slate-300 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>

          <button
            onClick={exportCSV}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-mono text-slate-300 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>CSV</span>
          </button>
        </div>
      </div>

      {/* Table Container */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/90 overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
              <tr>
                <th className="py-3 px-3 w-12 text-center">ID</th>
                <th className="py-3 px-4">Part Name</th>
                <th className="py-3 px-2 text-center">Qty</th>
                <th className="py-3 px-3">Lumber</th>
                <th className="py-3 px-3 text-right">Length</th>
                <th className="py-3 px-3 text-right">Width</th>
                <th className="py-3 px-3 text-right">Thick</th>
                <th className="py-3 px-2 text-center">Angle</th>
                <th className="py-3 px-4">Notes & Joinery</th>
                <th className="py-3 px-3 text-center">Confidence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {filtered.map((item, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3 px-3 text-center">
                    <span className="inline-block w-6 h-6 rounded bg-amber-500/10 text-amber-400 font-bold border border-amber-500/20 text-center leading-6">
                      {item.part_id}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-sans font-semibold text-white">
                    {item.part_name}
                  </td>
                  <td className="py-3 px-2 text-center font-bold text-amber-400">
                    {item.quantity}
                  </td>
                  <td className="py-3 px-3 text-slate-300">
                    {item.lumber_size}
                  </td>
                  <td className="py-3 px-3 text-right font-bold text-sky-400">
                    {item.length.toFixed(2)}"
                  </td>
                  <td className="py-3 px-3 text-right text-slate-400">
                    {item.width.toFixed(2)}"
                  </td>
                  <td className="py-3 px-3 text-right text-slate-400">
                    {item.thickness.toFixed(2)}"
                  </td>
                  <td className="py-3 px-2 text-center text-slate-400">
                    {item.angle}
                  </td>
                  <td className="py-3 px-4 text-slate-400 font-sans text-xs max-w-xs truncate">
                    {item.notes || 'Crosscut'}
                  </td>
                  <td className="py-3 px-3 text-center">
                    <span className={`text-[10px] px-2 py-0.5 rounded-full border ${
                      item.confidence === 'CONFIRMED'
                        ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        : item.confidence === 'USER_PROVIDED'
                        ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}>
                      {item.confidence}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
