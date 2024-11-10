# Game Mechanics Analysis Tool

A Python-based tool for analyzing and categorizing game mechanics from textual game descriptions using LLM (Large Language Model) technology.

## 🎯 Overview

This project provides a framework for analyzing game mechanics by processing game descriptions and categorizing them into meaningful patterns. It uses an LLM to identify core gameplay elements, player interactions, and game mechanics patterns.

## 🏗️ Architecture

The project consists of three main components:

### 1. Game Analysis Runner (`analyze_games.py`)
- Manages the overall analysis pipeline
- Handles loading and processing of game descriptions  
- Coordinates the analysis workflow
- Provides formatted output of results

### 2. Game Mechanics Processor (`core/game_mechanic_blocks.py`)
- Extracts core gameplay patterns
- Processes mechanics into structured categories
- Handles JSON processing and validation
- Formats analysis output

### 3. Game Mechanics Analyzer (`core/analyzer.py`) 
- Discovers and categorizes game actions andmechanics
- Clusters game actions and mechanics into categories
- Integrates with LLM client for analysis

## 🚀 Features

- Automated discovery of game mechanics categories
- LLM-powered analysis of gameplay patterns
- Clustering of similar mechanics
- JSON-based persistence of category descriptions
- Formatted output of analysis results
- Logging system for analysis tracking

## 📋 Requirements

- Python 3.x
- OpenAI API access (for LLM functionality)
- Required Python packages (specify in requirements.txt)

## 💻 Usage

```python
from analyze_games import GameAnalysisRunner
from pathlib import Path

# Initialize the runner
runner = GameAnalysisRunner(data_dir=Path("./data")) #change this to your csv path

# Run analysis on a sample of games
results = runner.run_analysis(num_games=3)
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
├── analyze_games.py
├── descriptors.csv # game name, description file mapping
├── desscriptors
│   ├── *.txt # game descriptions
├── core/
│   ├── analyzer.py
│   └── game_mechanic_blocks.py
├── discovery/
│   ├── mechanics_discovery.py
├── llm/
│   └── openai_client.py
├── clustering/
│   └── base.py
│   └── llm_clusterer.py

```


## 🔍 Future Improvements

- Support for additional LLM providers
- Enhanced clustering algorithms
- Interactive analysis interface

## 🎮 Sample Analysis Results

### Training Results

After processing 3 games (Minesweeper, Final Fantasy, and Castlevania), the system discovered 6 primary mechanic categories:

1. **Grid-based Puzzle Mechanics**
   - Description: This category involves mechanics where players interact with a grid or board to achieve specific objectives, often involving revealing or manipulating elements within the grid.

2. **Spatial Interaction**
   - Description: This category encompasses mechanics that involve interaction with a spatial environment, often requiring players to navigate, explore, or interpret information within a defined space.

3. **Hazard Avoidance**
   - Description: This category involves mechanics where players must identify, avoid, or manage potential dangers or obstacles within the game environment. These mechanics often require strategic planning and careful observation to prevent negative outcomes.

4. **Combat Systems**
   - Description: This category encompasses mechanics related to engaging in battles or fights within a game. It includes various methods and systems through which players interact with enemies, manage their characters, and utilize weapons or abilities to achieve victory.

5. **Progression Systems**
   - Description: Mechanics that involve the advancement or development of characters, players, or game states over time. These systems often provide a sense of growth, achievement, or escalation in difficulty.

6. **Resource and Inventory Management**
   - Description: This category involves managing resources and items that players collect and use throughout the game. It includes systems for equipping characters, organizing inventory, and utilizing items strategically to enhance gameplay.

### Core Gameplay Patterns

The analysis identified the following pattern categories:

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

## ⚠️ Notes

- Ensure proper API credentials are configured
- Large game descriptions may require additional processing time
- Results may vary based on LLM model used

---
