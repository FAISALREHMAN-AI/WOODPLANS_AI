import React, { useState } from 'react';
import { 
  ArrowLeft, 
  Edit3, 
  RefreshCw, 
  Download, 
  FileDown, 
  Layers, 
  Ruler, 
  Boxes, 
  Scissors, 
  ShoppingCart, 
  Wrench, 
  Compass, 
  FileSpreadsheet, 
  Calendar,
  Share2,
  Check
} from 'lucide-react';
import { Project } from '../../types';
import { OverviewTab } from '../tabs/OverviewTab';
import { DimensionsTab } from '../tabs/DimensionsTab';
import { ComponentsTab } from '../tabs/ComponentsTab';
import { CutListTab } from '../tabs/CutListTab';
import { MaterialsTab } from '../tabs/MaterialsTab';
import { HardwareTab } from '../tabs/HardwareTab';
import { JoineryTab } from '../tabs/JoineryTab';
import { BuildStepsTab } from '../tabs/BuildStepsTab';
import { DiagramsTab } from '../tabs/DiagramsTab';
import { PdfExportTab } from '../tabs/PdfExportTab';
import { EditProjectModal } from '../EditProjectModal';
import { apiClient } from '../../api/client';

interface ProjectDetailViewProps {
  project: Project;
  onBack: () => void;
  onUpdate: (updated: Partial<Project>) => Promise<void>;
  onReanalyze: (options: any) => Promise<void>;
}

export const ProjectDetailView: React.FC<ProjectDetailViewProps> = ({
  project,
  onBack,
  onUpdate,
  onReanalyze
}) => {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [isEditOpen, setIsEditOpen] = useState<boolean>(false);
  const [isCopied, setIsCopied] = useState<boolean>(false);

  const tabs = [
    { id: 'overview', label: 'PRODUCT OVERVIEW', icon: Layers },
    { id: 'dimensions', label: 'DIMENSIONS', icon: Ruler },
    { id: 'components', label: 'COMPONENTS', icon: Boxes },
    { id: 'cut_list', label: 'CUT LIST', icon: Scissors },
    { id: 'materials', label: 'MATERIALS', icon: ShoppingCart },
    { id: 'hardware', label: 'HARDWARE', icon: Wrench },
    { id: 'joinery', label: 'JOINERY', icon: Compass },
    { id: 'build_steps', label: 'BUILD STEPS', icon: FileSpreadsheet },
    { id: 'diagrams', label: 'DIAGRAMS', icon: Compass },
    { id: 'pdf_export', label: 'PDF EXPORT', icon: FileDown },
  ];

  const handleShare = () => {
    navigator.clipboard.writeText(window.location.href);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4 py-4">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="p-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-mono font-bold uppercase tracking-wider text-amber-500">
                {project.product_type || 'Custom DIY Build'}
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                READY TO BUILD
              </span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              {project.name}
            </h2>
          </div>
        </div>

        {/* Global Action Buttons */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setIsEditOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-mono font-medium transition-colors"
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>EDIT ANALYSIS</span>
          </button>

          <button
            onClick={() => setIsEditOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-amber-400 text-xs font-mono font-medium transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>RE-ANALYZE</span>
          </button>

          <a
            href={apiClient.getPdfUrl(project.id)}
            download={`${project.name.replace(/\s+/g, '_')}_plan.pdf`}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs font-mono transition-all shadow-md shadow-amber-500/20 active:scale-95"
          >
            <Download className="w-3.5 h-3.5" />
            <span>DOWNLOAD PDF</span>
          </a>
        </div>
      </div>

      {/* Tabs Navigation Bar */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-2 border-b border-slate-800 scrollbar-none">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-xs font-mono font-semibold transition-all whitespace-nowrap ${
                isActive
                  ? 'bg-amber-500/15 text-amber-400 border border-amber-500/30 shadow-inner'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
              }`}
            >
              <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-amber-500' : 'text-slate-400'}`} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* Active Tab Content Area */}
      <div className="pt-2">
        {activeTab === 'overview' && (
          <OverviewTab project={project} onOpenEdit={() => setIsEditOpen(true)} />
        )}
        {activeTab === 'dimensions' && (
          <DimensionsTab project={project} onOpenEdit={() => setIsEditOpen(true)} />
        )}
        {activeTab === 'components' && (
          <ComponentsTab components={project.components} />
        )}
        {activeTab === 'cut_list' && (
          <CutListTab cutList={project.cut_list_items} productName={project.name} />
        )}
        {activeTab === 'materials' && (
          <MaterialsTab
            materials={project.materials}
            wastePercentage={project.waste_percentage}
            onUpdateWaste={(pct) => onUpdate({ waste_percentage: pct })}
          />
        )}
        {activeTab === 'hardware' && (
          <HardwareTab hardware={project.hardware} />
        )}
        {activeTab === 'joinery' && (
          <JoineryTab components={project.components} />
        )}
        {activeTab === 'build_steps' && (
          <BuildStepsTab instructions={project.instructions} />
        )}
        {activeTab === 'diagrams' && (
          <DiagramsTab
            diagrams={project.diagrams}
            references={project.references}
            productName={project.name}
          />
        )}
        {activeTab === 'pdf_export' && (
          <PdfExportTab project={project} />
        )}
      </div>

      {/* Edit & Re-Analyze Modal */}
      <EditProjectModal
        project={project}
        isOpen={isEditOpen}
        onClose={() => setIsEditOpen(false)}
        onSave={onUpdate}
        onReanalyze={onReanalyze}
      />
    </div>
  );
};
