import json
from typing import List, Dict, Any
from llm.openai_client import OpenAIClient
import logging

logger = logging.getLogger(__name__)

class GameMechanicsProcessor:
    def __init__(self, llm_client):
        self.client = llm_client

    def load_json(self, filepath: str) -> List[Dict[str, str]]:
        """Load and validate game mechanics JSON"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded mechanics data with {len(data)} categories")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON: {str(e)}")
            raise

    def extract_core_patterns(self, categories: List[Dict[str, str]]) -> Dict[str, Any]:
        """Extract core gameplay patterns from categories"""
        prompt = """
        Analyze these game mechanic categories and identify core gameplay patterns.
        Return a JSON object with these keys:
        - core_mechanics: List of fundamental gameplay actions
        - player_interactions: List of ways players engage with the game
        - progression_elements: List of how players advance or improve
        - resource_types: List of resources players manage
        - challenge_patterns: List of common challenge types
        
        Categories to analyze:
        {}
        """.format(json.dumps(categories, indent=2))
        
        return self.client.call_api(prompt)

    
    def process_mechanics(self, filepath: str) -> Dict[str, Any]:
        """Process game mechanics file into core patterns only"""
        try:
            # Load categories
            categories = self.load_json(filepath)
            
            # Extract patterns
            logger.info("Extracting core patterns")
            patterns = self.extract_core_patterns(categories)
            
            return {"core_patterns": patterns}
            
        except Exception as e:
            logger.error(f"Error processing mechanics: {str(e)}")
            raise

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format results into readable text"""
        output = []
        
        # Core Patterns only
        output.append("CORE GAMEPLAY PATTERNS")
        for category, elements in result["core_patterns"].items():
            output.append(f"\n{category.title()}")
            for element in elements:
                output.append(f"- {element}")
        
        return "\n".join(output)

def process_game_mechanics(client, filepath: str, output_format: str = "json") -> Any:
    """
    Process game mechanics JSON file
    
    Args:
        client: OpenAIClient instance
        filepath: Path to JSON file
        output_format: "json" or "text"
    """
    processor = GameMechanicsProcessor(client)
    result = processor.process_mechanics(filepath)
    
    if output_format == "text":
        return processor.format_output(result)
    return result


if __name__ == "__main__":
    client = OpenAIClient()
    result = process_game_mechanics(client, "category_descriptions.json", "text")
    print(result)