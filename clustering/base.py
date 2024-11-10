from abc import ABC, abstractmethod
from typing import Dict, List, Any
from enum import Enum

class ClusteringMethod(Enum):
    DBSCAN = "dbscan"  # TODO: Implement DBSCAN clustering
    LLM = "llm"

class Clusterer(ABC):
    """Abstract base class for clustering methods."""
    
    @abstractmethod
    def cluster_mechanics(self, mechanics: List[Dict[str, str]]) -> Dict[int, List[Dict[str, str]]]:
        """Cluster mechanics into groups."""
        pass
