import React, { useState } from 'react';
import { FolderGit2, Search, Plus, Filter, HardDrive } from 'lucide-react';
import { Project } from '../../types';
import { ProjectCard } from '../ProjectCard';

interface MyProjectsViewProps {
  projects: Project[];
  onOpenProject: (id: string) => void;
  onEditProject: (project: Project) => void;
  onDeleteProject: (id: string) => void;
  onNewProject: () => void;
}

export const MyProjectsView: React.FC<MyProjectsViewProps> = ({
  projects,
  onOpenProject,
  onEditProject,
  onDeleteProject,
  onNewProject
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  const filtered = projects.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (p.product_type && p.product_type.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesStatus = filterStatus === 'all' || p.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4 py-4">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
            <FolderGit2 className="w-6 h-6 text-amber-500" />
            <span>My Woodworking Projects ({projects.length})</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Access your saved DIY woodworking plans, master cut lists, and CAD blueprints.
          </p>
        </div>

        <button
          onClick={onNewProject}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-medium text-xs font-mono transition-all shadow-md active:scale-95"
        >
          <Plus className="w-4 h-4" />
          <span>New Build Plan</span>
        </button>
      </div>

      {/* Search & Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-3 rounded-xl bg-slate-900 border border-slate-800">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search by project name or product type..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-amber-500"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-300 font-mono focus:border-amber-500"
          >
            <option value="all">All Statuses</option>
            <option value="analyzed">Analyzed (CAD Ready)</option>
            <option value="draft">Drafts</option>
          </select>
        </div>
      </div>

      {/* Project Grid */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(proj => (
            <ProjectCard
              key={proj.id}
              project={proj}
              onOpen={onOpenProject}
              onEdit={onEditProject}
              onDelete={onDeleteProject}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-16 p-8 rounded-2xl border border-dashed border-slate-800 bg-slate-900/40 space-y-3">
          <HardDrive className="w-12 h-12 text-slate-600 mx-auto" />
          <h4 className="text-sm font-semibold text-slate-300">No Projects Found</h4>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            {searchTerm ? 'No projects match your search criteria.' : 'Create your first woodworking plan by dropping a reference image or PDF.'}
          </p>
          <button
            onClick={onNewProject}
            className="mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-medium text-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Create New Plan</span>
          </button>
        </div>
      )}
    </div>
  );
};
