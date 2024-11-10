import json
import logging
from typing import Dict, List, Any
from llm.base import LLMClient
from clustering.base import ClusteringMethod, Clusterer
from clustering.dbscan import DBSCANClusterer
from clustering.llm_clusterer import LLMClusterer

logger = logging.getLogger(__name__)

class MechanicDiscovery:
    """Discovers mechanic categories and patterns from game descriptions."""
    
    def __init__(self, 
                 llm_client: LLMClient, 
                 clustering_method: ClusteringMethod = ClusteringMethod.DBSCAN,
                 dbscan_params: Dict[str, float] = None):
        self.llm = llm_client
        self.clustering_method = clustering_method
        
        if clustering_method == ClusteringMethod.DBSCAN:
            params = dbscan_params or {"eps": 0.5, "min_samples": 2}
            self.clusterer = DBSCANClusterer(**params)
        else:
            self.clusterer = LLMClusterer(llm_client)
    
    def extract_raw_mechanics(self, game_description: str) -> List[Dict[str, str]]:
        """Extract mechanics from a single game description."""
        prompt = f"""
        Analyze this game description and extract every specific gameplay mechanic.
        Return a JSON object with this structure:
        {{
            "mechanics": [
                {{
                    "mechanic": "exact quote",
                    "concept": "core action or behavior",
                    "description": "detailed description"
                }},
                ...
            ]
        }}
        
        Game description: {game_description}
        """
        
        try:
            response = self.llm.call_api(prompt)
            return response.get('mechanics', [])
        except Exception as e:
            logger.error(f"Failed to extract mechanics: {str(e)}")
            return []

    def discover_categories(self, game_descriptions: List[str]) -> Dict[str, Any]:
        """Discover mechanic categories from multiple game descriptions."""
        # Extract mechanics from all games
        all_mechanics = []
        for description in game_descriptions:
            mechanics = self.extract_raw_mechanics(description)
            all_mechanics.extend(mechanics)
            
        # Cluster mechanics using selected method
        clusters = self.clusterer.cluster_mechanics(all_mechanics)
        
        # Analyze clusters to determine categories
        categories = {}
        for cluster_id, mechanics in clusters.items():
            category = self._analyze_cluster(mechanics)
            categories[category['name']] = category
            
        return categories
    
    def _analyze_cluster(self, mechanics: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze a cluster of mechanics to determine its category."""
        mechanics_json = json.dumps(mechanics)
        prompt = f"""
        Analyze these related game mechanics and determine their common category:
        {{
            "name": "brief category name",
            "description": "detailed category description",
            "common_elements": ["shared characteristics"],
            "key_variations": ["major variations within category"],
            "example_mechanics": ["representative examples"]
        }}

        Mechanics: {mechanics_json}
        """
        
        try:
            return self.llm.call_api(prompt)
        except Exception as e:
            logger.error(f"Failed to analyze cluster: {str(e)}")
            return {
                "name": "Unknown",
                "description": "Failed to analyze cluster",
                "common_elements": [],
                "key_variations": [],
                "example_mechanics": []
            }