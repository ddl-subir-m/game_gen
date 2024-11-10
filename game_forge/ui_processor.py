from typing import Dict, List, Any
import json
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Any, Dict
import sys

sys.path.append('/Users/subir.mansukhani/Desktop/game_gen')
from llm.openai_client import OpenAIClient

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MechanicsUIProcessor:
    def __init__(self, llm_client):
        self.client = llm_client
        
    def get_ai_decision(self, element_name: str, context: str) -> bool:
        """
        Use LLM to decide if an element needs a scale based on context.
        """
        prompt = f"""Analyze the game design element "{element_name}" within the category "{context}" to determine if it should be a scale (1-5) or toggle (on/off) control.

        Evaluation Framework:
        1. Quantifiable Variation:
           - Does the element have meaningful intermediate states between on/off?
           - Are there clear distinctions between different levels of intensity?

        2. Player Impact:
           - Would different levels meaningfully change the gameplay experience?
           - Would players benefit from fine-grained control over this element?

        3. Implementation Feasibility:
           - Can the element be practically implemented with multiple levels?
           - Would each scale point (1,2,3,4,5) represent a distinct, implementable state?

        4. Design Clarity:
           - Would players understand what each scale point means?
           - Is there a clear progression from 1 to 5?

        Examples:
        - "combat_difficulty" needs a scale because it has clear intermediate states and impacts gameplay significantly
        - "permadeath" needs a toggle because it's a binary feature without meaningful intermediate states
        - "resource_scarcity" needs a scale because different levels of scarcity create different gameplay experiences

        Return a JSON object with:
        {{
            "needs_scale": boolean,
            "reasoning": "detailed justification addressing the above criteria",
            "confidence": float (0.0-1.0)
        }}

        Only assign a scale if the element meets at least 3 of the 4 criteria with high confidence (>0.8).
        Default to toggle if there's significant uncertainty."""
        
        try:
            response = self.client.call_api(prompt)
            # Only return true if confidence is high enough
            confidence = response.get('confidence', 0.0)
            needs_scale = response.get('needs_scale', False)
            
            if confidence >= 0.8 and needs_scale:
                # logger.info(f"Assigned scale to {element_name} with confidence {confidence}: {response.get('reasoning', 'No reasoning provided')}")
                return True
            else:
                # logger.info(f"Assigned toggle to {element_name} with confidence {confidence}: {response.get('reasoning', 'No reasoning provided')}")
                return False
                
        except Exception as e:
            logger.warning(f"Error getting AI decision for {element_name}: {str(e)}")
            return False
            
    def process_elements(self, elements: List[str], section_name: str) -> List[Dict[str, Any]]:
        """Process list of elements using AI for scale decisions"""
        processed = []
        for element in elements:
            element_info = {
                'name': element,
                'display_name': element.replace('_', ' ').title(),
            }
            
            needs_scale = self.get_ai_decision(element, section_name)
            
            if needs_scale:
                element_info.update({
                    'input_type': 'scale',
                    'scale': {
                        'min': 1,
                        'max': 5,
                        'default': 3,
                        'step': 1
                    }
                })
            else:
                element_info.update({
                    'input_type': 'toggle',
                    'default': False
                })
                
            processed.append(element_info)
        return processed
    
    def process_game_design_elements(self, input_json: Dict[str, List[str]]) -> Dict[str, Any]:
        """Process game design elements using AI to determine which need scales."""
        output_structure = {}
        for section, elements in input_json.items():
            output_structure[section] = {
                'display_name': section.replace('_', ' ').title(),
                'elements': self.process_elements(elements, section)
            }
        
        return output_structure

def main():
    # Example usage
    input_json = {
        "core_mechanics": [
            "grid_manipulation",
            "spatial_navigation",
            "hazard_identification",
            "combat_engagement",
            "character_development",
            "resource_allocation"
        ],
        "player_interactions": [
            "grid_interaction",
            "environment_exploration",
            "obstacle_avoidance",
            "enemy_encounter",
            "skill_upgrading",
            "inventory_management"
        ],
        "progression_elements": [
            "level_completion",
            "skill_tree_advancement",
            "experience_gain",
            "story_unfolding",
            "equipment_upgrade"
        ],
        "resource_types": [
            "puzzle_pieces",
            "navigation_tools",
            "health_and_safety_items",
            "weapons_and_armor",
            "experience_points",
            "inventory_items"
        ],
        "challenge_patterns": [
            "puzzle_solving",
            "spatial_puzzles",
            "timed_avoidance",
            "enemy_defeat",
            "level_difficulty_increase",
            "resource_scarcity"
        ]
    }
    
    # Initialize OpenAI client and processor
    client = OpenAIClient(model="gpt-4o")  
    processor = MechanicsUIProcessor(client)
    
    # Process the game design elements
    result = processor.process_game_design_elements(input_json)
    
    logger.info("Processed game design elements:\n%s", json.dumps(result, indent=2))
    
    # Optionally save to file
    with open('processed_mechanics.json', 'w') as f:
        json.dump(result, f, indent=2)
        logger.info("Results saved to processed_mechanics.json")

if __name__ == "__main__":
    main()