import json
import logging
from .base import Clusterer
from llm.base import LLMClient


from typing import Dict, List

logger = logging.getLogger(__name__)

class LLMClusterer(Clusterer):
    """LLM-based clustering implementation."""
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        
    def cluster_mechanics(self, mechanics: List[Dict[str, str]]) -> Dict[int, List[Dict[str, str]]]:
        # Extract just the concepts for the prompt
        concepts = [m["concept"] for m in mechanics]
        
        prompt = f"""
        Analyze these game mechanics and group them into natural categories.
        Return a JSON object where each key is a category number and the value is a list of mechanic indices.
        Only include mechanics that fit clearly into categories.
        
        Example format:
        {{
            "clusters": {{
                "0": [0, 3, 5],  // indices of concepts in first cluster
                "1": [1, 4],     // indices of concepts in second cluster
                "2": [2, 6]      // indices of concepts in third cluster
            }},
            "category_descriptions": {{
                "0": "description of first category",
                "1": "description of second category",
                "2": "description of third category"
            }}
        }}

        Concepts: {json.dumps(concepts)}
        """
        
        try:
            response = self.llm.call_api(prompt)
            clusters = response.get('clusters', {})
            # Map the concept indices back to the original mechanic objects
            return {
                int(k): [mechanics[idx] for idx in v]
                for k, v in clusters.items()
            }
        except Exception as e:
            logger.error(f"Failed to cluster mechanics: {str(e)}")
            return {}