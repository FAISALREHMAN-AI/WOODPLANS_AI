import React, { useState } from 'react';
import { 
  FileDown, 
  Printer, 
  ExternalLink, 
  CheckCircle2, 
  Layers, 
  RefreshCw,
  Ruler,
  Compass,
  Boxes
} from 'lucide-react';
import { Project } from '../../types';
import { apiClient, API_BASE } from '../../api/client';

interface PdfExportTabProps {
  project: Project;
}

export const PdfExportTab: React.FC<PdfExportTabProps> = ({ project }) => {
  const [isGenerating, setIsGenerating] = useState(false);
  const pdfUrl = apiClient.getPdfUrl(project.id);

  const handleRegeneratePdf = async () => {
    setIsGenerating(true);
    try {
      await fetch(`${API_BASE}/api/projects/${project.id}/generate-pdf`, {
        method: 'POST'
      });
      // Force iframe refresh
      const iframe = document.getElementById('pdf-preview-frame') as HTMLIFrameElement;
      if (iframe) iframe.src = `${pdfUrl}?t=${Date.now()}`;
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Blueprint Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-500">
              TRADITIONAL CONSTRUCTION MANUAL
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              BLACK &amp; WHITE ONLY
            </span>
          </div>
          <h3 className="text-base sm:text-lg font-bold text-white flex items-center gap-2 mt-0.5">
            <Printer className="w-5 h-5 text-slate-300" />
            <span>Printable Construction Blueprint Plan</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5 font-mono">
            Optimized for standard B&amp;W home/shop printers  •  Footer on every page: <strong className="text-white">TIMBER SHOP BY FAISAL</strong>
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={handleRegeneratePdf}
            disabled={isGenerating}
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono font-medium transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? 'animate-spin' : ''}`} />
            <span>Recompile Blueprint</span>
          </button>

          <a
            href={pdfUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-mono font-medium transition-colors"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Open in Tab</span>
          </a>

          <a
            href={pdfUrl}
            download={`${project.name.replace(/\s+/g, '_')}_blueprint.pdf`}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-white hover:bg-slate-200 text-slate-950 font-bold text-xs font-mono transition-all shadow-md active:scale-95"
          >
            <FileDown className="w-4 h-4" />
            <span>Download B&amp;W Blueprint PDF</span>
          </a>
        </div>
      </div>

      {/* Blueprint Feature Badges */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono text-slate-300">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-slate-400" />
          <span>Cover &amp; Grayscale Photo</span>
        </div>
        <div className="flex items-center gap-2">
          <Boxes className="w-4 h-4 text-slate-400" />
          <span>Individual Part Blueprints</span>
        </div>
        <div className="flex items-center gap-2">
          <Compass className="w-4 h-4 text-slate-400" />
          <span>Exploded View &amp; Joinery</span>
        </div>
        <div className="flex items-center gap-2">
          <Ruler className="w-4 h-4 text-slate-400" />
          <span>8-Ft Cutting Layouts</span>
        </div>
      </div>

      {/* PDF Embedded Frame */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950 overflow-hidden shadow-2xl h-[700px] relative">
        <iframe
          id="pdf-preview-frame"
          src={pdfUrl}
          className="w-full h-full border-none"
          title="B&W Woodworking Blueprint PDF Preview"
        />
      </div>
    </div>
  );
};
