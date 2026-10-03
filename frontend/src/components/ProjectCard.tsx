import React from 'react';
import { 
  FileText, 
  Download, 
  Trash2, 
  Edit3, 
  RefreshCw, 
  Calendar, 
  Ruler, 
  Layers,
  ArrowUpRight,
  ShieldCheck
} from 'lucide-react';
import { Project } from '../types';
import { apiClient } from '../api/client';

interface ProjectCardProps {
  project: Project;
  onOpen: (id: string) => void;
  onEdit: (project: Project) => void;
  onDelete: (id: string) => void;
}

export const ProjectCard: React.FC<ProjectCardProps> = ({ project, onOpen, onEdit, onDelete }) => {
  const primaryRef = project.references.find(r => r.is_primary) || project.references[0];
  const hasPdf = project.status === 'analyzed';

  return (
    <div className="group rounded-2xl border border-slate-800 bg-slate-900/80 hover:border-slate-700 hover:bg-slate-900 transition-all duration-200 overflow-hidden shadow-lg flex flex-col justify-between">
      {/* Thumbnail area */}
      <div 
        onClick={() => onOpen(project.id)}
        className="h-44 bg-slate-950 relative overflow-hidden cursor-pointer flex items-center justify-center border-b border-slate-800/80"
      >
        {primaryRef && !primaryRef.file_type.includes('pdf') ? (
          <img
            src={apiClient.getFileUrl(primaryRef.file_url)}
            alt={project.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="flex flex-col items-center justify-center p-6 text-center">
            <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-500 mb-2">
              <FileText className="w-6 h-6" />
            </div>
            <span className="text-xs font-mono text-slate-400">
              {project.reference_type === 'pdf' ? 'PDF Blueprint Attached' : 'CAD Plan Ready'}
            </span>
          </div>
        )}

        {/* Status Badge */}
        <div className="absolute top-3 left-3">
          <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider backdrop-blur-md border ${
            project.status === 'analyzed'
              ? 'bg-emerald-950/80 text-emerald-400 border-emerald-500/30'
              : project.status === 'analyzing'
              ? 'bg-amber-950/80 text-amber-400 border-amber-500/30 animate-pulse'
              : 'bg-slate-900/80 text-slate-400 border-slate-700'
          }`}>
            {project.status === 'analyzed' ? 'CAD READY' : project.status}
          </span>
        </div>

        {/* Quick Open Icon */}
        <div className="absolute bottom-3 right-3 w-8 h-8 rounded-full bg-slate-900/90 text-white flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200 border border-slate-700 shadow-md">
          <ArrowUpRight className="w-4 h-4" />
        </div>
      </div>

      {/* Info Body */}
      <div className="p-5 space-y-3 flex-1 flex flex-col justify-between">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-[11px] font-mono font-semibold uppercase tracking-wider text-amber-500">
              {project.product_type || 'Custom DIY Build'}
            </span>
          </div>

          <h4 
            onClick={() => onOpen(project.id)}
            className="text-base font-bold text-white group-hover:text-amber-400 transition-colors line-clamp-1 cursor-pointer"
          >
            {project.name}
          </h4>

          {/* Envelope Dimensions Badge */}
          {project.overall_width ? (
            <div className="flex items-center gap-1.5 text-xs font-mono text-slate-300 pt-1">
              <Ruler className="w-3.5 h-3.5 text-sky-400" />
              <span>{project.overall_width}" W × {project.overall_depth}" D × {project.overall_height}" H</span>
            </div>
          ) : (
            <p className="text-xs text-slate-500 italic">Dimensions pending analysis</p>
          )}
        </div>

        {/* Date & Meta */}
        <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-500 font-mono">
          <div className="flex items-center gap-1">
            <Calendar className="w-3.5 h-3.5" />
            <span>{new Date(project.created_at).toLocaleDateString()}</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => onEdit(project)}
              className="p-1.5 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200 transition-colors"
              title="Edit Dimensions"
            >
              <Edit3 className="w-3.5 h-3.5" />
            </button>

            {hasPdf && (
              <a
                href={apiClient.getPdfUrl(project.id)}
                download
                className="p-1.5 rounded-lg hover:bg-amber-500/20 text-slate-400 hover:text-amber-400 transition-colors"
                title="Download PDF Woodworking Plan"
              >
                <Download className="w-3.5 h-3.5" />
              </a>
            )}

            <button
              onClick={() => onDelete(project.id)}
              className="p-1.5 rounded-lg hover:bg-red-500/20 text-slate-400 hover:text-red-400 transition-colors"
              title="Delete Project"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
