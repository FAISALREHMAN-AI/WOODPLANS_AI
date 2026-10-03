import React from 'react';
import { Compass, Hammer, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { ComponentItem } from '../../types';

interface JoineryTabProps {
  components: ComponentItem[];
}

export const JoineryTab: React.FC<JoineryTabProps> = ({ components }) => {
  // Derive joinery pairs from components
  const joints = components.map((c, idx) => ({
    joint_id: `J-${idx + 1}`,
    component: `Part ${c.part_id} (${c.part_name})`,
    joint_type: c.joinery || 'Pocket-Hole Butt Joint',
    fastener: c.hardware || '1-1/4" Pocket Screws & Glue',
    location: `Mating end faces of ${c.part_name}`,
    direction: 'Internal concealed face boring',
    status: 'Likely joinery — verify before construction'
  }));

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Compass className="w-5 h-5 text-amber-500" />
            <span>Joinery Methods & Fastening Topology</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Engineering connections specifying joint types, fastener specs, and assembly orientations.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {joints.map((joint, idx) => (
          <div
            key={idx}
            className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-amber-400 px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20">
                {joint.joint_id}
              </span>
              <span className="text-[10px] font-mono text-slate-400 italic">
                {joint.status}
              </span>
            </div>

            <div>
              <h4 className="text-sm font-bold text-white">{joint.joint_type}</h4>
              <p className="text-xs font-mono text-sky-400 mt-0.5">{joint.component}</p>
            </div>

            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-xs font-mono space-y-1 text-slate-300">
              <div className="flex justify-between">
                <span className="text-slate-500">Fastener Spec:</span>
                <span className="text-slate-200">{joint.fastener}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Joint Location:</span>
                <span className="text-slate-200">{joint.location}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Assembly Vector:</span>
                <span className="text-slate-200">{joint.direction}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
