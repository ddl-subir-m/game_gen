import json
import logging
import random
import csv
import os
from pathlib import Path

from core import GameMechanicsAnalyzer, GameMechanicsProcessor, save_category_descriptions
from llm.openai_client import OpenAIClient
from clustering.base import ClusteringMethod
from game_forge.ui_processor import MechanicsUIProcessor
from game_forge.story_gen import GameMechanicsSelector, generate_game_concepts, save_generated_stories

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GameAnalysisRunner:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.analyzer = GameMechanicsAnalyzer(
            llm_client=OpenAIClient(),
            clustering_method=ClusteringMethod.LLM
        )
        # Add class logger
        self.logger = logging.getLogger(__name__)
    
    def load_game_descriptions(self) -> dict:
        """Load game descriptions from CSV and corresponding text files."""
        csv_path = self.data_dir / 'descriptors.csv'
        descriptors_dir = self.data_dir / 'descriptors'
        games = {}
        
        with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                desc_path = descriptors_dir / row['Descriptor']
                if desc_path.exists():
                    games[row['Game']] = desc_path.read_text(encoding='utf-8')
        
        return games

    @staticmethod
    def print_analysis_results(analysis: dict, title: str = "Analysis Results"):
        """Helper function to pretty print analysis results."""
        print("\n" + "="*50)
        print(f"{title}")
        print("="*50)
        print(json.dumps(analysis, indent=2))
        print("="*50 + "\n")

    def print_training_summary(self, training_results: dict):
        """Print training results in a formatted way."""
        print("\n" + "="*50)
        print("Training Results")
        print("="*50)
        print(f"Processed {training_results['total_games']} games")
        print(f"Discovered {len(training_results['categories'])} categories\n")

        print("Categories discovered:")
        for i, category in enumerate(training_results['categories'], 1):
            print(f"\n{i}. {category['name']}")
            if category['description']:
                print(f"   Description: {category['description']}")
        print("="*50 + "\n")

    def run_analysis(self, num_games: int = 3):
        """Run the complete analysis pipeline."""
        # Load and select games
        games = self.load_game_descriptions()
        selected_games = random.sample(list(games.keys()), num_games)
        
        # Log selected games
        self.logger.info("Selected games for analysis:")
        for i, game in enumerate(selected_games, 1):
            self.logger.info(f"{i}. {game}")

        # First pass of the analyzer
        self.logger.info("Starting analyzer first pass...")
        training_results = self.analyzer.first_pass(selected_games)
        self.print_training_summary(training_results)

        # Save results
        self.logger.info("Saving category descriptions...")
        save_category_descriptions(
            training_results['categories'],
            self.data_dir / 'category_descriptions.json'
        )

        # Process mechanics patterns
        self.logger.info("Processing game mechanics patterns...")
        processor = GameMechanicsProcessor(self.analyzer.llm)
        patterns = processor.extract_core_patterns(training_results['categories'])
        
        # Print results
        self.print_analysis_results(patterns, "Core Gameplay Patterns")
        return patterns

def main():
    data_dir = Path(".")  # Adjust this path as needed
    runner = GameAnalysisRunner(data_dir)
    
    # Get the analysis patterns
    patterns = runner.run_analysis()
    
    # Initialize UI processor
    processor = MechanicsUIProcessor(OpenAIClient(model="gpt-4o"))
    
    # Process the game design elements
    mechanics_json = processor.process_game_design_elements(patterns)
    
    # Save to file
    with open('processed_mechanics.json', 'w') as f:
        json.dump(mechanics_json, f, indent=2)
    
    # For testing select a subset of mechanics and generate game concepts
    selector = GameMechanicsSelector(mechanics_json)
    selected_mechanics = selector.get_random_subset(complexity=3)
    # Generate game concepts
    return generate_game_concepts(selected_mechanics)

if __name__ == "__main__":
    generated_stories = main()
    save_generated_stories(generated_stories)