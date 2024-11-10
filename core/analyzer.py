import json
import logging
from typing import Dict, List, Any
from llm.base import LLMClient
from clustering.base import ClusteringMethod
from discovery.mechanic_discovery import MechanicDiscovery

logger = logging.getLogger(__name__)

def save_category_descriptions(categories: list, output_file: str = 'category_descriptions.json'):
    """Save category descriptions to a JSON file."""
    descriptions = [
        {
            'name': category['name'],
            'description': category['description']
        }
        for category in categories
    ]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(descriptions, f, indent=2)

class GameMechanicsAnalyzer:
    """Game mechanics analyzer using discovered categories."""
    
    def __init__(self, 
                 llm_client: LLMClient,
                 clustering_method: ClusteringMethod = ClusteringMethod.LLM,
                 dbscan_params: Dict[str, float] = None):
        self.llm = llm_client
        self.discovery = MechanicDiscovery(
            llm_client, 
            clustering_method,
        )
        self.categories = None
        
    def first_pass(self, game_descriptions: List[str]):
        """Discover categories from a training set of game descriptions."""
        logger.info(f"Starting training on {len(game_descriptions)} game descriptions")
        
        # Extract mechanics from each training game uncomment for testing and comment discover_categories

        # all_mechanics = []
        # for i, desc in enumerate(game_descriptions, 1):
        #     logger.info(f"Processing training game {i}...")
        #     mechanics = self.discovery.extract_raw_mechanics(desc)
        #     all_mechanics.extend(mechanics)
        #     logger.info(f"Found {len(mechanics)} mechanics in game {i}")
        
        # logger.info(f"Total mechanics extracted: {len(all_mechanics)}")
        
        # Discover categories
        logger.info("Discovering categories...")
        self.categories = self.discovery.discover_categories(game_descriptions)
        
        # Log category details
        logger.info(f"Training complete - discovered {len(self.categories)} categories:")
        return {
            'total_games': len(game_descriptions),
            'categories': [
                {
                    'name': category_info['name'],
                    'description': category_info['description']
                }
                for category_info in self.categories.values()
            ]
        }
    

    
    