import React from 'react';
import { Settings, Cpu, Database, Cloud, ShieldCheck, CheckCircle2, Server, Globe } from 'lucide-react';
import { API_BASE } from '../../api/client';

export const SettingsView: React.FC = () => {
  const apiUrl = API_BASE || window.location.origin;

  return (
    <div className="space-y-6 max-w-4xl mx-auto px-4 py-4">
      <div>
        <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-amber-500" />
          <span>Application Settings & System Architecture</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Configuration parameters, cloud backend telemetry, and AI model orchestration.
        </p>
      </div>

      {/* AI Engine Status */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <Cpu className="w-5 h-5 text-amber-500" />
            <div>
              <h4 className="text-sm font-bold text-white">AI Vision & Decomposition Engine</h4>
              <p className="text-xs text-slate-400">Multi-modal structural reasoning and parametric solver</p>
            </div>
          </div>
          <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
            HEALTHY & ACTIVE
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
            <span className="text-slate-500 block">PRIMARY PROVIDER</span>
            <span className="text-slate-200 font-bold">Google Gemini 1.5 / 2.5 Flash Vision</span>
            <p className="text-[11px] text-slate-400 font-sans">
              Analyzes reference images & PDF pages for joints, lumber, and features.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
            <span className="text-slate-500 block">PARAMETRIC SOLVER</span>
            <span className="text-slate-200 font-bold">WoodPlan CAD Knowledge Engine</span>
            <p className="text-[11px] text-slate-400 font-sans">
              Rule-based geometric calculator for cut lists, 15% waste, and SVG diagrams.
            </p>
          </div>
        </div>
      </div>

      {/* Deployment & Environment */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
          <Server className="w-5 h-5 text-sky-400" />
          <div>
            <h4 className="text-sm font-bold text-white">Production Deployment Endpoints</h4>
            <p className="text-xs text-slate-400">Current API connectivity and deployment target</p>
          </div>
        </div>

        <div className="space-y-3 text-xs font-mono">
          <div className="flex justify-between items-center p-3 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-400">Backend API URL (VITE_API_URL):</span>
            <span className="text-amber-400 font-bold">{apiUrl}</span>
          </div>

          <div className="flex justify-between items-center p-3 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-400">Frontend Platform:</span>
            <span className="text-slate-200">Vercel (React + Vite + Tailwind)</span>
          </div>

          <div className="flex justify-between items-center p-3 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-400">Backend Platform:</span>
            <span className="text-slate-200">Render (Python FastAPI + ReportLab)</span>
          </div>

          <div className="flex justify-between items-center p-3 rounded-xl bg-slate-950 border border-slate-800">
            <span className="text-slate-400">Database Engine:</span>
            <span className="text-slate-200">PostgreSQL (SQLAlchemy ORM + SQLite dev fallback)</span>
          </div>
        </div>
      </div>
    </div>
  );
};
