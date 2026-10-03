import { Project, ProgressState, ScaleAnchorData } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = {
  async listProjects(): Promise<Project[]> {
    const res = await fetch(`${API_BASE}/api/projects`);
    if (!res.ok) throw new Error('Failed to load projects');
    return res.json();
  },

  async getProject(id: string): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects/${id}`);
    if (!res.ok) throw new Error(`Project ${id} not found`);
    return res.json();
  },

  async createProject(name?: string, description?: string): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description }),
    });
    if (!res.ok) throw new Error('Failed to create project');
    return res.json();
  },

  async uploadReference(projectId: string, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_BASE}/api/projects/${projectId}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to upload reference file');
    }
    return res.json();
  },

  async deleteReference(projectId: string, refId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/references/${refId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete reference');
    return res.json();
  },

  async getProgress(projectId: string): Promise<ProgressState> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/progress`);
    if (!res.ok) return { step: 'Processing...', percentage: 0 };
    return res.json();
  },

  async startAnalysis(
    projectId: string,
    options?: {
      scaleAnchor?: ScaleAnchorData;
      customWidth?: number;
      customDepth?: number;
      customHeight?: number;
      wastePercentage?: number;
    }
  ): Promise<any> {
    const formData = new FormData();
    if (options?.scaleAnchor) {
      formData.append('scale_anchor_type', options.scaleAnchor.anchor_type);
      formData.append('scale_anchor_value', options.scaleAnchor.anchor_dimension_value.toString());
      formData.append('scale_anchor_axis', options.scaleAnchor.anchor_axis);
    }
    if (options?.customWidth) formData.append('custom_width', options.customWidth.toString());
    if (options?.customDepth) formData.append('custom_depth', options.customDepth.toString());
    if (options?.customHeight) formData.append('custom_height', options.customHeight.toString());
    if (options?.wastePercentage) formData.append('waste_percentage', options.wastePercentage.toString());

    const res = await fetch(`${API_BASE}/api/projects/${projectId}/analyze`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Analysis failed');
    }
    return res.json();
  },

  async reanalyze(projectId: string, payload: any): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}/reanalyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to re-analyze project');
    return res.json();
  },

  async updateProject(projectId: string, payload: Partial<Project>): Promise<Project> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error('Failed to update project');
    return res.json();
  },

  async deleteProject(projectId: string): Promise<any> {
    const res = await fetch(`${API_BASE}/api/projects/${projectId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete project');
    return res.json();
  },

  getPdfUrl(projectId: string): string {
    return `${API_BASE}/api/projects/${projectId}/pdf`;
  },

  getFileUrl(urlPath?: string): string {
    if (!urlPath) return '';
    if (urlPath.startsWith('http')) return urlPath;
    return `${API_BASE}${urlPath}`;
  }
};
