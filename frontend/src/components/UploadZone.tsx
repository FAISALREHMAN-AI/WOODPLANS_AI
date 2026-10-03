import React, { useState, useRef, useEffect } from 'react';
import { 
  UploadCloud, 
  FileText, 
  Image as ImageIcon, 
  Trash2, 
  Plus, 
  Layers, 
  Ruler, 
  CheckCircle2, 
  AlertCircle,
  HelpCircle,
  ClipboardPaste,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { ScaleAnchorData } from '../types';

interface UploadZoneProps {
  onAnalyze: (files: File[], anchor?: ScaleAnchorData, manualDims?: any) => void;
  isAnalyzing: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onAnalyze, isAnalyzing }) => {
  const [files, setFiles] = useState<{ file: File; preview: string; isPdf: boolean }[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Dimension & Scale Anchor States
  const [anchorType, setAnchorType] = useState<string>('none');
  const [anchorAxis, setAnchorAxis] = useState<'width' | 'depth' | 'height'>('width');
  const [customAnchorVal, setCustomAnchorVal] = useState<string>('75');
  const [anchorDesc, setAnchorDesc] = useState<string>('');

  // Manual dimensions override
  const [manualWidth, setManualWidth] = useState<string>('');
  const [manualDepth, setManualDepth] = useState<string>('');
  const [manualHeight, setManualHeight] = useState<string>('');
  const [wastePct, setWastePct] = useState<number>(15);
  const [showAdvanced, setShowAdvanced] = useState<boolean>(false);

  // Clipboard Paste Support
  useEffect(() => {
    const handlePaste = (e: ClipboardEvent) => {
      if (e.clipboardData && e.clipboardData.items) {
        for (let i = 0; i < e.clipboardData.items.length; i++) {
          const item = e.clipboardData.items[i];
          if (item.type.indexOf('image') !== -1) {
            const blob = item.getAsFile();
            if (blob) {
              const file = new File([blob], `pasted_reference_${Date.now()}.png`, { type: blob.type });
              addFiles([file]);
            }
          }
        }
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  const addFiles = (newFiles: File[]) => {
    const valid = newFiles.filter(f => {
      const ext = f.name.toLowerCase();
      return ext.endsWith('.jpg') || ext.endsWith('.jpeg') || ext.endsWith('.png') || ext.endsWith('.webp') || ext.endsWith('.pdf');
    });

    const mapped = valid.map(file => {
      const isPdf = file.name.toLowerCase().endsWith('.pdf');
      const preview = isPdf ? '' : URL.createObjectURL(file);
      return { file, preview, isPdf };
    });

    setFiles(prev => [...prev, ...mapped]);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      addFiles(Array.from(e.dataTransfer.files));
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => {
      const copy = [...prev];
      if (copy[index].preview) URL.revokeObjectURL(copy[index].preview);
      copy.splice(index, 1);
      return copy;
    });
  };

  const handleStartAnalysis = () => {
    if (files.length === 0) return;

    let scaleAnchor: ScaleAnchorData | undefined;
    if (anchorType !== 'none') {
      let val = 75;
      if (anchorType === 'mattress_twin') val = 75;
      else if (anchorType === 'mattress_full') val = 75;
      else if (anchorType === 'mattress_queen') val = 80;
      else if (anchorType === '2x4_stud') val = 3.5;
      else if (anchorType === 'custom') val = parseFloat(customAnchorVal) || 75;

      scaleAnchor = {
        anchor_type: anchorType,
        anchor_dimension_value: val,
        anchor_axis: anchorAxis,
        description: anchorDesc || `Anchored to ${anchorType}`
      };
    }

    const manualDims: any = {};
    if (manualWidth) manualDims.customWidth = parseFloat(manualWidth);
    if (manualDepth) manualDims.customDepth = parseFloat(manualDepth);
    if (manualHeight) manualDims.customHeight = parseFloat(manualHeight);
    manualDims.wastePercentage = wastePct;

    onAnalyze(files.map(f => f.file), scaleAnchor, manualDims);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Dropzone Card */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 relative overflow-hidden ${
          isDragging
            ? 'border-amber-500 bg-amber-500/10 scale-[1.01]'
            : 'border-slate-700 bg-slate-900/60 hover:border-slate-500 hover:bg-slate-900/90'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".jpg,.jpeg,.png,.webp,.pdf"
          className="hidden"
          onChange={(e) => {
            if (e.target.files) addFiles(Array.from(e.target.files));
          }}
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500/20 to-amber-700/20 border border-amber-500/30 flex items-center justify-center shadow-inner">
            <UploadCloud className="w-8 h-8 text-amber-400" />
          </div>

          <div>
            <h3 className="text-lg font-semibold text-white">
              Drop woodworking photo, blueprint, or PDF here
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              or browse your files • <span className="text-amber-400 font-medium">Ctrl+V</span> to paste screenshot from clipboard
            </p>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs font-mono text-slate-500">
            <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">JPG</span>
            <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">JPEG</span>
            <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">PNG</span>
            <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">WEBP</span>
            <span className="px-2 py-0.5 rounded bg-amber-950/60 border border-amber-600/40 text-amber-300 font-semibold">PDF PLAN</span>
          </div>
        </div>
      </div>

      {/* Uploaded Files Previews */}
      {files.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-400">
              Loaded References ({files.length})
            </span>
            <button
              onClick={() => fileInputRef.current?.click()}
              className="text-xs text-amber-400 hover:text-amber-300 flex items-center gap-1 font-medium"
            >
              <Plus className="w-3.5 h-3.5" />
              Add Another Reference
            </button>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {files.map((item, idx) => (
              <div
                key={idx}
                className="group relative rounded-xl border border-slate-800 bg-slate-900/90 overflow-hidden shadow-md flex flex-col justify-between"
              >
                {item.isPdf ? (
                  <div className="h-32 flex flex-col items-center justify-center bg-slate-950/60 p-3 text-center">
                    <FileText className="w-10 h-10 text-amber-500 mb-1" />
                    <span className="text-[11px] font-mono text-slate-300 line-clamp-1">{item.file.name}</span>
                    <span className="text-[10px] text-slate-500">{(item.file.size / 1024).toFixed(0)} KB</span>
                  </div>
                ) : (
                  <div className="h-32 w-full bg-slate-950 relative overflow-hidden">
                    <img src={item.preview} alt="Reference" className="w-full h-full object-cover" />
                  </div>
                )}

                <div className="p-2 border-t border-slate-800 flex items-center justify-between text-xs bg-slate-900">
                  <span className="truncate max-w-[100px] text-slate-400 text-[11px]">
                    {item.file.name}
                  </span>
                  <button
                    onClick={(e) => { e.stopPropagation(); removeFile(idx); }}
                    className="p-1 rounded hover:bg-red-500/20 text-slate-500 hover:text-red-400 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dimension Inference & Scale Anchor System */}
      <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2">
              <Ruler className="w-4 h-4 text-amber-400" />
              <h4 className="text-sm font-semibold text-white">Scale Anchor & Dimension Inference</h4>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                Recommended
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Select a known standard component or enter a measurement to anchor the AI's dimensional scale.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="text-xs font-medium text-slate-300 block mb-1.5">Known Object / Reference</label>
            <select
              value={anchorType}
              onChange={(e) => setAnchorType(e.target.value)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
            >
              <option value="none">No Anchor (AI Estimate Only)</option>
              <option value="mattress_twin">Twin Mattress (38" × 75")</option>
              <option value="mattress_full">Full Mattress (54" × 75")</option>
              <option value="mattress_queen">Queen Mattress (60" × 80")</option>
              <option value="2x4_stud">2x4 Nominal Lumber Width (3.5")</option>
              <option value="custom">Custom Dimension Anchor</option>
            </select>
          </div>

          {anchorType === 'custom' && (
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1.5">Dimension (Inches)</label>
              <input
                type="number"
                value={customAnchorVal}
                onChange={(e) => setCustomAnchorVal(e.target.value)}
                placeholder="e.g. 72"
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
              />
            </div>
          )}

          {anchorType !== 'none' && (
            <div>
              <label className="text-xs font-medium text-slate-300 block mb-1.5">Reference Axis</label>
              <select
                value={anchorAxis}
                onChange={(e) => setAnchorAxis(e.target.value as any)}
                className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
              >
                <option value="width">Along Width (Horizontal span)</option>
                <option value="depth">Along Depth (Front-to-back)</option>
                <option value="height">Along Height (Vertical)</option>
              </select>
            </div>
          )}
        </div>

        {/* Advanced Manual Dimension Overrides */}
        <div className="pt-2 border-t border-slate-800">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1 font-mono"
          >
            <span>{showAdvanced ? '▼ Hide' : '▶ Show'} Manual Dimension Overrides (Optional)</span>
          </button>

          {showAdvanced && (
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-3">
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">Target Width (in)</label>
                <input
                  type="number"
                  placeholder="e.g. 79.5"
                  value={manualWidth}
                  onChange={(e) => setManualWidth(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">Target Depth (in)</label>
                <input
                  type="number"
                  placeholder="e.g. 42.0"
                  value={manualDepth}
                  onChange={(e) => setManualDepth(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">Target Height (in)</label>
                <input
                  type="number"
                  placeholder="e.g. 72.0"
                  value={manualHeight}
                  onChange={(e) => setManualHeight(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono"
                />
              </div>
              <div>
                <label className="text-[11px] font-mono text-slate-400 block mb-1">Waste Allowance (%)</label>
                <input
                  type="number"
                  value={wastePct}
                  onChange={(e) => setWastePct(parseFloat(e.target.value) || 15)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 font-mono"
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Analyze Action Bar */}
      <div className="flex items-center justify-between pt-2">
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <AlertCircle className="w-4 h-4 text-amber-500 shrink-0" />
          <span>Plans are AI estimates. Dry-fit and verify dimensions before permanent cuts.</span>
        </div>

        <button
          onClick={handleStartAnalysis}
          disabled={files.length === 0 || isAnalyzing}
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-sm transition-all shadow-lg ${
            files.length === 0 || isAnalyzing
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              : 'bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold active:scale-95 shadow-amber-500/20'
          }`}
        >
          <Sparkles className="w-4 h-4" />
          <span>{isAnalyzing ? 'Analyzing Reference...' : 'Analyze Project & Generate Plan'}</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
