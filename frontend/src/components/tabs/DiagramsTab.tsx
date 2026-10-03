import React from 'react';
import { Compass } from 'lucide-react';
import { DiagramItem, ReferenceItem } from '../../types';
import { BlueprintViewer } from '../BlueprintViewer';

interface DiagramsTabProps {
  diagrams: DiagramItem[];
  references: ReferenceItem[];
  productName: string;
}

export const DiagramsTab: React.FC<DiagramsTabProps> = ({ diagrams, references, productName }) => {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Compass className="w-5 h-5 text-amber-500" />
          <span>Technical CAD Blueprints & Multiview Drafting</span>
        </h3>
        <p className="text-xs text-slate-400 mt-1">
          Precision orthographic projections, exploded axonometric views, and joinery details with drafting arrows and extension lines.
        </p>
      </div>

      <BlueprintViewer
        diagrams={diagrams}
        references={references}
        productName={productName}
      />
    </div>
  );
};
