import React from 'react';
import { 
  Hammer, 
  Sparkles, 
  Ruler, 
  Layers, 
  FileCheck2, 
  ShieldCheck, 
  ArrowRight,
  Boxes,
  FileSpreadsheet,
  CheckCircle2
} from 'lucide-react';
import { UploadZone } from '../UploadZone';
import { AnalysisProgress } from '../AnalysisProgress';
import { ScaleAnchorData } from '../../types';

interface NewProjectViewProps {
  onAnalyze: (files: File[], anchor?: ScaleAnchorData, manualDims?: any) => void;
  isAnalyzing: boolean;
  progressStep: string;
  progressPct: number;
}

export const NewProjectView: React.FC<NewProjectViewProps> = ({
  onAnalyze,
  isAnalyzing,
  progressStep,
  progressPct
}) => {
  return (
    <div className="py-6 space-y-12 max-w-5xl mx-auto px-4">
      {/* Hero Section */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-mono font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Next-Gen Woodworking Computer Vision & Plan Synthesis</span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Turn Any Woodworking Reference Into a <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-amber-500 to-amber-600">Ready-to-Build Plan</span>.
        </h1>

        <p className="text-base sm:text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto">
          Upload a photo or existing PDF plan. WOODPLAN AI analyzes the structural components, lumber sizing, joinery, and generates complete cut lists with CAD blueprints.
        </p>

        {/* Feature badges */}
        <div className="flex flex-wrap items-center justify-center gap-4 pt-2 text-xs font-mono text-slate-300">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Scale Anchor Inference
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Master Cut Lists
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Technical CAD SVGs
          </span>
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Printable PDF Manual
          </span>
        </div>
      </div>

      {/* Main Analysis Card / Progress */}
      {isAnalyzing ? (
        <AnalysisProgress currentStep={progressStep} percentage={progressPct} />
      ) : (
        <UploadZone onAnalyze={onAnalyze} isAnalyzing={isAnalyzing} />
      )}

      {/* Supported Products Grid */}
      <div className="pt-8 border-t border-slate-800 space-y-4">
        <div className="text-center">
          <h4 className="text-xs font-mono font-semibold uppercase tracking-wider text-slate-500">
            Engineered For All Wooden DIY Builds
          </h4>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 gap-2.5 text-center text-xs font-mono text-slate-400">
          {[
            'House Beds & Cribs', 'Farmhouse Tables', 'Workshop Benches',
            'Adirondack Chairs', 'Built-in Shelves', 'Kitchen Cabinets',
            'Garden Planters', 'Chicken Coops', 'Backyard Sheds',
            'Patio Pergolas', 'Shoe Racks & Benches', 'Kids Play Furniture'
          ].map((item, idx) => (
            <div key={idx} className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800/80 hover:border-slate-700 transition-colors">
              {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
