import json
from pathlib import Path
from datetime import datetime
import random
from typing import Dict, Any, List
import sys
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

sys.path.append('/Users/subir.mansukhani/Desktop/game_gen')
from llm.openai_client import OpenAIClient

class GameMechanicsSelector:
    def __init__(self, base_json: Dict[str, Any]):
        self.base_json = base_json
        self.categories = list(base_json.keys())
        
    def get_random_subset(self, complexity: int = 3) -> Dict[str, Any]:
        """Generate a random subset of mechanics with given complexity."""
        selected = {}
        
        for category, content in self.base_json.items():
            if isinstance(content, dict) and 'elements' in content:
                selected[category] = {
                    'display_name': content['display_name'],
                    'elements': []
                }
                
                num_elements = min(complexity, len(content['elements']))
                chosen_elements = random.sample(content['elements'], num_elements)
                
                for element in chosen_elements:
                    element_copy = element.copy()
                    if element['input_type'] == 'scale':
                        element_copy['value'] = random.randint(
                            element['scale']['min'],
                            element['scale']['max']
                        )
                    else:  # toggle
                        element_copy['value'] = random.choice([True, False])
                    selected[category]['elements'].append(element_copy)
        
        return selected

class GameStoryGenerator:
    def __init__(self, llm_client: OpenAIClient):
        self.llm_client = llm_client
        self.generated_stories = []
        self.min_score_threshold = 3.0  # Minimum acceptable score
        self.max_regeneration_attempts = 3
        
    def _format_mechanics_for_prompt(self, mechanics: Dict[str, Any]) -> str:
        """Format the mechanics into a readable string for the prompt."""
        formatted = []
        for category, content in mechanics.items():
            formatted.append(f"\n{content['display_name']}:")
            for element in content['elements']:
                value = element['value']
                if isinstance(value, bool):
                    value_str = "Enabled" if value else "Disabled"
                else:
                    value_str = f"Level {value} out of 5"
                formatted.append(f"- {element['display_name']}: {value_str}")
        
        return "\n".join(formatted)

    def _evaluate_story(self, story: str, mechanics: Dict[str, Any]) -> float:
        """Evaluate the generated story and return a score between 1 and 5."""
        # Get story text from the dictionary
        try:
            story_text = story["story"]
        except (TypeError, KeyError):
            logger.error("Story missing or invalid format")
            return 1.0

        formatted_mechanics = self._format_mechanics_for_prompt(mechanics)
        
        prompt = f"""Evaluate the following game concept based on the given mechanics. 
Consider creativity, coherence, and how well it utilizes the mechanics.

Game Mechanics:{formatted_mechanics}

Game Concept:
{story_text}

Scoring Rubric:
5.0: Outstanding
- Exceptional creativity and originality
- All mechanics are deeply integrated and interact meaningfully
- Clear, engaging gameplay loop with compelling progression
- Unique selling points are well-defined
- Mechanics combinations create emergent gameplay possibilities

4.0: Good
- Creative concept with some unique elements
- Most mechanics are well integrated
- Solid gameplay loop and progression
- Clear value proposition
- Mechanics work together cohesively

3.0: Average
- Standard concept with some interesting elements
- Basic integration of mechanics
- Functional gameplay loop
- Limited uniqueness
- Mechanics mostly work independently

2.0: Below Average
- Derivative or unclear concept
- Poor integration of mechanics
- Weak gameplay loop
- Lacks distinctiveness
- Mechanics feel disconnected

1.0: Poor
- Incoherent or incomplete concept
- Mechanics are ignored or misused
- No clear gameplay loop
- Highly derivative
- Mechanics conflict or make no sense together

Rate this concept on a scale of 1.0 to 5.0 based on the rubric above.

Provide your response as a JSON object with the following structure:
{{
    "score": <float between 1.0 and 5.0>,
    "reasoning": "Brief explanation of the score based on the rubric criteria"
}}

Ensure your response is a valid JSON object."""

        try:
            response = self.llm_client.call_api(prompt)
            return float(response["score"])
        except Exception as e:
            logger.error(f"Error evaluating story: {str(e)}")
            return 1.0  # Return lowest score on error

    def generate_story(self, mechanics: Dict[str, Any]) -> str:
        """Generate a game story and regenerate if quality is below threshold."""
        attempts = 0
        best_story = None
        best_score = 0
        formatted_mechanics = self._format_mechanics_for_prompt(mechanics)

        while attempts < self.max_regeneration_attempts:
            attempts += 1
            
            try:
                prompt = f"""Given the following game mechanics and their values, generate a detailed and creative game description.
Include specific gameplay examples and how these mechanics interact with each other to create engaging experiences.

Game Mechanics:{formatted_mechanics}

Generate a response that covers:
1. Core gameplay loop and how the mechanics work together
2. Specific examples of interesting gameplay scenarios
3. How the difficulty and complexity progress
4. What makes this combination of mechanics unique and engaging

Please write in a clear, engaging style similar to a game design document or review.

Provide your response as a JSON object with the following structure:
{{
    "story": "Your complete game description here"
}}

Ensure your response is a valid JSON object."""

                story = self.llm_client.call_api(prompt)
                score = self._evaluate_story(story, mechanics)
                
                logger.info(f"Story generation attempt {attempts}, score: {score}")
                
                if score > best_score:
                    best_score = score
                    best_story = story
                
                if score >= self.min_score_threshold:
                    break
                    
            except Exception as e:
                logger.error(f"Error in generation attempt {attempts}: {str(e)}")
                continue

        final_story = best_story or "Failed to generate an acceptable story"
        
        self.generated_stories.append({
            'mechanics': mechanics,
            'story': final_story,
            'score': best_score,
            'attempts': attempts
        })
        
        return final_story

def generate_game_concepts(mechanics_json: Dict[str, Any], num_concepts: int = 3) -> List[Dict]:
    """Generate game concepts from the provided mechanics JSON.
    
    Args:
        mechanics_json: Processed mechanics in JSON format
        num_concepts: Number of concepts to generate
    
    Returns:
        List of generated stories with their mechanics
    """
    # Initialize OpenAI client
    sys_msg = (
        "You are a creative game designer who specializes in creating "
        "unique game concepts from mechanical elements. Generate engaging "
        "and detailed game descriptions based on the provided mechanics."
    )
    llm_client = OpenAIClient(model="gpt-4o", system_message=sys_msg)
    
    # Create instances
    selector = GameMechanicsSelector(mechanics_json)
    generator = GameStoryGenerator(llm_client)
    
    logger.info(f"Generating {num_concepts} different game concepts...")
    
    for i in range(num_concepts):
        logger.info(f"\n{'='*20} Game Concept {i+1} {'='*20}")
        
        # Generate random subset of mechanics
        selected_mechanics = selector.get_random_subset(complexity=3)
        
        # Log selected mechanics
        logger.info("Selected Mechanics:")
        for category, content in selected_mechanics.items():
            logger.info(f"\n{content['display_name']}:")
            for element in content['elements']:
                value_str = "Enabled" if isinstance(element['value'], bool) and element['value'] else \
                           "Disabled" if isinstance(element['value'], bool) else \
                           f"Level {element['value']} out of 5"
                logger.info(f"- {element['display_name']}: {value_str}")
        
        # Generate and log story
        logger.info("\nGame Concept:")
        logger.info("-" * 50)
        story = generator.generate_story(selected_mechanics)
        logger.info(story)
        logger.info("\n" + "="*60 + "\n")
    
    return generator.generated_stories

def save_generated_stories(stories: List[Dict[str, Any]], base_dir: str = "stories") -> None:
    """Save generated stories to JSON files in the specified directory.
    
    Args:
        stories: List of generated story dictionaries
        base_dir: Base directory to save stories (default: 'stories')
    """
    stories_dir = Path(base_dir)
    stories_dir.mkdir(exist_ok=True)
    
    # Save individual stories
    for i, story_data in enumerate(stories, 1):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"story_{i}_{timestamp}.json"
        
        with open(stories_dir / filename, 'w', encoding='utf-8') as f:
            json.dump({
                'story': story_data['story'],
                'mechanics': story_data['mechanics'],
                'score': story_data['score'],
                'attempts': story_data['attempts'],
                'generation_time': timestamp
            }, f, indent=2, ensure_ascii=False)
    
    # Save summary file
    summary_file = stories_dir / f"stories_summary_{datetime.now().strftime('%Y%m%d')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_stories': len(stories),
            'generation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }, f, indent=2, ensure_ascii=False)


def main():
    # Load the base mechanics JSON
    try:
        with open('processed_mechanics.json', 'r') as f:
            mechanics_json = json.load(f)
    except FileNotFoundError:
        logger.error("Could not find processed_mechanics.json")
        return

    return generate_game_concepts(mechanics_json, num_concepts=1)

if __name__ == "__main__":
    generated_stories = main()
    save_generated_stories(generated_stories)