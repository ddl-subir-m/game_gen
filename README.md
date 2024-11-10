# Game Mechanics Analysis and Generation Tool

A Python-based tool for analyzing and categorizing game mechanics from textual game descriptions using LLM (Large Language Model) technology.

## 🎯 Overview

This project provides a framework for analyzing game mechanics by processing game descriptions and categorizing them into meaningful patterns. It uses an LLM to identify core gameplay elements, player interactions, and game mechanics patterns.

## 🏗️ Architecture

The project consists of five main components:

### 1. Game Analysis Runner (`analyze_games.py`)
- Manages the overall analysis pipeline
- Handles loading and processing of game descriptions  
- Coordinates the analysis workflow
- Provides formatted output of results

### 2. Game Mechanics Analyzer (`core/analyzer.py`) 
- Discovers and categorizes game actions and mechanics
- Clusters game actions and mechanics into categories and describes the clusters
- Integrates with LLM client for analysis

### 3. Game Mechanics Processor (`core/game_mechanic_blocks.py`)
- Extracts core gameplay patterns from initial set of game mechanics and category descriptions
- Processes mechanics into structured categories
- Handles JSON processing and validation
- Formats analysis output

### 4. MechanicsUIProcessor (`game_forge/ui_processor.py`)
- Processes game mechanics and determines appropriate UI controls
- Uses LLM to decide between scale (1-5) and toggle controls
- Handles JSON processing and validation

### 5. GameStoryGenerator (`game_forge/story_gen.py`)
- Generates creative game concepts from mechanics combinations
- Provides scoring and feedback on generated concepts
- Includes regeneration of game stories based on quality evaluation


## 🚀 Features

- Automated discovery of game mechanics categories
- LLM-powered analysis of gameplay patterns
- Clustering of similar mechanics
- Automated UI control type determination
- Story generation with quality assessment
- Automatic story regeneration for low-quality outputs

## 📋 Requirements

- Python 3.11.x
- OpenAI API access (for LLM functionality)
- Required Python packages (specify in requirements.txt)

## 💻 Usage

```python
from analyze_gen_games import GameAnalysisRunner
from core import GameMechanicsAnalyzer, GameMechanicsProcessor, save_category_descriptions
from game_forge.ui_processor import MechanicsUIProcessor
from llm.openai_client import OpenAIClient
from pathlib import Path

# Initialize the runner
runner = GameAnalysisRunner(data_dir=Path("./data")) #change this to your csv path

# Run analysis on a sample of games
results = runner.run_analysis(num_games=3)

# Initialize UI processor
processor = MechanicsUIProcessor(OpenAIClient(model="gpt-4o"))

# Process the game design elements
mechanics_json = processor.process_game_design_elements(patterns)

# For testing select a subset of mechanics and generate game concepts
selector = GameMechanicsSelector(mechanics_json)
selected_mechanics = selector.get_random_subset(complexity=3)

# Generate game concepts
generated_stories = generate_game_concepts(selected_mechanics)

# Save the generated game concepts
save_generated_stories(generated_stories)
```

## 📊 Output Format

The analysis produces structured output including:

```json
{
  "core_mechanics": [],
  "player_interactions": [],
  "progression_elements": [],
  "resource_types": [],
  "challenge_patterns": []
}
```

## 🔧 Configuration

The tool can be configured through:
- LLM client settings
- Clustering method selection
- Category description parameters
- Analysis sample size

## 📁 Project Structure

```
.
├── analyze_gen_games.py
├── descriptors.csv # game name, description file mapping
├── desscriptors
│   ├── *.txt # game descriptions
├── core/
│   ├── analyzer.py
│   └── game_mechanic_blocks.py
├── clustering/
│   └── base.py
│   └── llm_clusterer.py
├── discovery/
│   ├── mechanics_discovery.py
├── game_forge/
│   ├── ui_processor.py
│   └── story_gen.py
├── llm/
│   └── openai_client.py

```


## 🔍 Future Improvements

- Support for additional LLM providers
- Enhanced clustering algorithms
- Interactive analysis interface
- Generate game code from game concepts
## 🎮 Sample Analysis Results

### Game Mechanics Analysis Results

After processing 3 games (Minesweeper, Final Fantasy, and Castlevania), the system identified the following game mechanics and patterns:

```json
{
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
```

### Game Concept Results
See the sample JSON output from game concept generation saved in the `stories` folder.

## ⚠️ Notes

- Ensure proper API credentials are configured
- Set the LLM API key in a .env file or in an environment variable
- Large game descriptions may require additional processing time
- Results may vary based on LLM model used. Only OpenAI models are supported at this time.
- Update the path in `game_forge/ui_processor.py` and `game_forge/story_gen.py` to point to the root of the project
---
