import React, { useState } from 'react';
import { 
  Eye, 
  Layers, 
  Maximize2, 
  Download, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw,
  SplitSquareVertical,
  Compass
} from 'lucide-react';
import { DiagramItem, ReferenceItem } from '../types';
import { apiClient } from '../api/client';

interface BlueprintViewerProps {
  diagrams: DiagramItem[];
  references: ReferenceItem[];
  productName: string;
}

export const BlueprintViewer: React.FC<BlueprintViewerProps> = ({ diagrams, references, productName }) => {
  const [activeView, setActiveView] = useState<string>('front');
  const [zoomLevel, setZoomLevel] = useState<number>(100);
  const [comparisonMode, setComparisonMode] = useState<boolean>(false);

  const currentDiagram = diagrams.find(d => d.view_type === activeView) || diagrams[0];
  const primaryRef = references.find(r => r.is_primary) || references[0];

  const handleDownloadSvg = () => {
    if (!currentDiagram) return;
    const blob = new Blob([currentDiagram.svg_content], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${productName.replace(/\s+/g, '_')}_${currentDiagram.view_type}_blueprint.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/90 overflow-hidden shadow-2xl flex flex-col">
      {/* Top CAD Drafting Toolbar */}
      <div className="px-4 py-3 border-b border-slate-800 bg-slate-950 flex flex-wrap items-center justify-between gap-3">
        {/* View Switchers */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {[
            { id: 'front', label: 'Front Elevation' },
            { id: 'side', label: 'Side Profile' },
            { id: 'top', label: 'Top / Plan' },
            { id: 'exploded', label: 'Exploded View' },
            { id: 'joinery', label: 'Joinery Details' },
          ].map((tab) => {
            const hasDiagram = diagrams.some(d => d.view_type === tab.id);
            const isActive = activeView === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveView(tab.id)}
                disabled={!hasDiagram}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-sky-500/20 text-sky-300 border border-sky-400/30 font-bold'
                    : hasDiagram
                    ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    : 'text-slate-600 cursor-not-allowed'
                }`}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {references.length > 0 && (
            <button
              onClick={() => setComparisonMode(!comparisonMode)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                comparisonMode
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                  : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
              }`}
            >
              <SplitSquareVertical className="w-3.5 h-3.5" />
              <span>{comparisonMode ? 'Single View' : 'Compare Reference'}</span>
            </button>
          )}

          <div className="flex items-center border border-slate-800 rounded-lg bg-slate-900 p-0.5">
            <button
              onClick={() => setZoomLevel(prev => Math.max(prev - 15, 60))}
              className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
              title="Zoom Out"
            >
              <ZoomOut className="w-3.5 h-3.5" />
            </button>
            <span className="text-[10px] font-mono text-slate-400 px-1.5">{zoomLevel}%</span>
            <button
              onClick={() => setZoomLevel(prev => Math.min(prev + 15, 180))}
              className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
              title="Zoom In"
            >
              <ZoomIn className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setZoomLevel(100)}
              className="p-1.5 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
              title="Reset Zoom"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>

          <button
            onClick={handleDownloadSvg}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono"
            title="Export Vector SVG"
          >
            <Download className="w-3.5 h-3.5" />
            <span>SVG</span>
          </button>
        </div>
      </div>

      {/* Main Canvas Viewport */}
      <div className={`p-4 min-h-[440px] flex items-center justify-center overflow-auto ${comparisonMode ? 'grid grid-cols-1 lg:grid-cols-2 gap-4' : ''}`}>
        {/* Reference Image in Comparison Mode */}
        {comparisonMode && primaryRef && (
          <div className="flex flex-col h-full rounded-xl border border-slate-800 bg-slate-950 overflow-hidden">
            <div className="px-3 py-2 border-b border-slate-800 text-xs font-mono text-slate-400 flex items-center justify-between">
              <span>SOURCE REFERENCE</span>
              <span className="text-amber-400">{primaryRef.file_name}</span>
            </div>
            <div className="flex-1 min-h-[350px] flex items-center justify-center p-4 bg-slate-900/40">
              {primaryRef.file_type.includes('pdf') ? (
                <div className="text-center p-8">
                  <Layers className="w-12 h-12 text-amber-500 mx-auto mb-2 opacity-60" />
                  <p className="text-xs font-mono text-slate-400">PDF Reference Source Attached</p>
                </div>
              ) : (
                <img
                  src={apiClient.getFileUrl(primaryRef.file_url)}
                  alt="Reference"
                  className="max-h-[420px] max-w-full object-contain rounded-lg shadow-lg border border-slate-800"
                />
              )}
            </div>
          </div>
        )}

        {/* Blueprint SVG Canvas */}
        <div className="w-full flex flex-col items-center justify-center rounded-xl overflow-hidden">
          {currentDiagram ? (
            <div
              className="w-full transition-transform duration-150 origin-center"
              style={{ transform: `scale(${zoomLevel / 100})` }}
              dangerouslySetInnerHTML={{ __html: currentDiagram.svg_content }}
            />
          ) : (
            <div className="p-12 text-center text-slate-500 font-mono text-xs">
              Generating blueprint views...
            </div>
          )}
        </div>
      </div>

      {/* Blueprint Subtitle Info */}
      {currentDiagram?.description && (
        <div className="px-4 py-2.5 bg-slate-950 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between font-mono">
          <span>{currentDiagram.description}</span>
          <span className="text-sky-400 font-semibold uppercase">{currentDiagram.view_type} VIEW</span>
        </div>
      )}
    </div>
  );
};
