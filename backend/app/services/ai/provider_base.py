from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseVisionProvider(ABC):
    @abstractmethod
    async def analyze_reference(
        self,
        file_path: str,
        file_type: str,
        scale_anchor: Optional[Dict[str, Any]] = None,
        custom_notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze reference image or PDF and return structured woodworking specification.
        """
        pass

class BaseTextProvider(ABC):
    @abstractmethod
    async def generate_build_plan(
        self,
        product_spec: Dict[str, Any],
        scale_anchor: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Takes product specification and expands into full build instructions, cut list, and joinery.
        """
        pass

class AIProvider(ABC):
    @abstractmethod
    async def process_woodworking_project(
        self,
        references: List[Dict[str, Any]],
        scale_anchor: Optional[Dict[str, Any]] = None,
        custom_dims: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        High-level orchestrator method returning the comprehensive project schema.
        """
        pass
