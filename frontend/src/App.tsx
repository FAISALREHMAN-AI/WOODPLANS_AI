import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { NewProjectView } from './components/views/NewProjectView';
import { ProjectDetailView } from './components/views/ProjectDetailView';
import { MyProjectsView } from './components/views/MyProjectsView';
import { SettingsView } from './components/views/SettingsView';
import { Project, ScaleAnchorData } from './types';
import { apiClient } from './api/client';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<string>('new_project');
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeProject, setActiveProject] = useState<Project | null>(null);
  
  // Progress states
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [progressStep, setProgressStep] = useState<string>('Initializing analysis...');
  const [progressPct, setProgressPct] = useState<number>(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Fetch projects on mount
  const loadProjects = async () => {
    try {
      const list = await apiClient.listProjects();
      setProjects(list);
    } catch (err: any) {
      console.warn('Backend offline or loading:', err.message);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleStartAnalysis = async (files: File[], anchor?: ScaleAnchorData, manualDims?: any) => {
    setIsAnalyzing(true);
    setProgressStep('Uploading reference images and plans...');
    setProgressPct(10);
    setErrorMsg(null);

    try {
      // Step 1: Create project in backend
      const primaryFile = files[0];
      const initialName = primaryFile.name.replace(/\.[^/.]+$/, "").replace(/[-_]/g, " ");
      const project = await apiClient.createProject(initialName);

      // Step 2: Upload all reference files
      for (let i = 0; i < files.length; i++) {
        setProgressStep(`Uploading reference ${i + 1} of ${files.length}...`);
        await apiClient.uploadReference(project.id, files[i]);
      }

      // Step 3: Trigger real backend analysis & start progress polling
      const pollInterval = setInterval(async () => {
        try {
          const prog = await apiClient.getProgress(project.id);
          if (prog) {
            setProgressStep(prog.step);
            setProgressPct(prog.percentage);
          }
        } catch (e) {
          // ignore transient poll error
        }
      }, 600);

      try {
        await apiClient.startAnalysis(project.id, {
          scaleAnchor: anchor,
          customWidth: manualDims?.customWidth,
          customDepth: manualDims?.customDepth,
          customHeight: manualDims?.customHeight,
          wastePercentage: manualDims?.wastePercentage,
        });
      } finally {
        clearInterval(pollInterval);
      }

      // Step 4: Load final analyzed project
      const finalProject = await apiClient.getProject(project.id);
      setActiveProject(finalProject);
      await loadProjects();
      setCurrentView('project_detail');
    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred during project analysis.');
    } finally {
      setIsAnalyzing(false);
      setProgressPct(0);
    }
  };

  const handleOpenProject = async (id: string) => {
    try {
      const proj = await apiClient.getProject(id);
      setActiveProject(proj);
      setCurrentView('project_detail');
    } catch (err: any) {
      setErrorMsg('Failed to open project.');
    }
  };

  const handleUpdateProject = async (updated: Partial<Project>) => {
    if (!activeProject) return;
    try {
      const res = await apiClient.updateProject(activeProject.id, updated);
      setActiveProject(res);
      await loadProjects();
    } catch (err: any) {
      setErrorMsg('Failed to save project updates.');
    }
  };

  const handleReanalyzeProject = async (options: any) => {
    if (!activeProject) return;
    setIsAnalyzing(true);
    try {
      const res = await apiClient.reanalyze(activeProject.id, options);
      setActiveProject(res);
      await loadProjects();
    } catch (err: any) {
      setErrorMsg('Re-analysis failed: ' + err.message);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDeleteProject = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this woodworking plan?')) return;
    try {
      await apiClient.deleteProject(id);
      await loadProjects();
      if (activeProject?.id === id) {
        setActiveProject(null);
        setCurrentView('my_projects');
      }
    } catch (err: any) {
      setErrorMsg('Failed to delete project.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans">
      {/* Top Navbar */}
      <Navbar
        currentView={currentView}
        onNavigate={(view) => {
          setCurrentView(view);
          if (view !== 'project_detail') setActiveProject(null);
        }}
        onNewProject={() => {
          setActiveProject(null);
          setCurrentView('new_project');
        }}
      />

      {/* Error Toast */}
      {errorMsg && (
        <div className="bg-red-500/10 border-b border-red-500/20 px-4 py-2.5 text-center text-xs text-red-300 font-mono flex items-center justify-center gap-2">
          <span>{errorMsg}</span>
          <button onClick={() => setErrorMsg(null)} className="underline hover:text-white ml-2">
            Dismiss
          </button>
        </div>
      )}

      {/* Main Workspace */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar */}
        <Sidebar
          currentView={currentView}
          onNavigate={(view) => {
            setCurrentView(view);
            if (view !== 'project_detail') setActiveProject(null);
          }}
          projectCount={projects.length}
        />

        {/* View Routing */}
        <main className="flex-1 overflow-y-auto blueprint-grid p-2 sm:p-4 md:p-6">
          {currentView === 'new_project' && (
            <NewProjectView
              onAnalyze={handleStartAnalysis}
              isAnalyzing={isAnalyzing}
              progressStep={progressStep}
              progressPct={progressPct}
            />
          )}

          {currentView === 'project_detail' && activeProject && (
            <ProjectDetailView
              project={activeProject}
              onBack={() => setCurrentView('my_projects')}
              onUpdate={handleUpdateProject}
              onReanalyze={handleReanalyzeProject}
            />
          )}

          {(currentView === 'my_projects' || currentView === 'recent_analyses' || currentView === 'generated_plans') && (
            <MyProjectsView
              projects={projects}
              onOpenProject={handleOpenProject}
              onEditProject={(p) => {
                setActiveProject(p);
                setCurrentView('project_detail');
              }}
              onDeleteProject={handleDeleteProject}
              onNewProject={() => setCurrentView('new_project')}
            />
          )}

          {currentView === 'settings' && <SettingsView />}
        </main>
      </div>
    </div>
  );
};

export default App;
