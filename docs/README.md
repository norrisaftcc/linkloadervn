# Link Loader Planning Directory

This directory contains the revised script and planning documents for the Link Loader visual novel, along with development tools for testing scripts outside of the Ren'Py engine.

## Script Files

- **script.md**: The main narrative script in Markdown format, containing all dialogue, scenes, and choices in an easy-to-read format. This is the "source of truth" for the story content.
- **script.rpy**: A partially-implemented version of the script in Ren'Py format, focusing on the core structure.
- **playable_script.rpy**: A complete implementation of the script in Ren'Py format, ready to be used in the game engine.
- **improvements.md**: A summary of all improvements made to the original script.

## Development Tools

### Quick Start - Play Link Loader in Text Mode

The easiest way to test Link Loader without the Ren'Py engine:

```bash
cd planning
python play_linkloader.py
```

### Available Tools

1. **renpy_game_player.py**: Full game player for testing complete Ren'Py games
   - Loads all .rpy files in a game directory
   - Supports save/load, history, and debug features
   - Interactive menu choices

2. **renpy_player.py**: Simple player for individual script files
   - Basic script parsing and playback
   - Good for testing single scenes

3. **dialogue_player.py**: JSON-based dialogue tree player
   - Node-based conversation flow
   - Variable tracking and conditions

4. **script_streamlit.py**: Web-based script player
   - Visual interface using Streamlit
   - Character stats display

5. **convert_script.py**: Convert between script formats
   - Ren'Py ↔ JSON ↔ Markdown conversions

### Usage Examples

```bash
# Play Link Loader in text mode
python renpy_game_player.py ../renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game

# Test a single script file
python renpy_player.py test_script.rpy

# Convert script formats
python convert_script.py --input script.rpy --output script.json --format renpy2json
```

## How to Use These Files

1. **For Story Editing**:
   - Make changes to `script.md` first to focus on narrative structure and dialogue
   - This keeps the story separate from implementation details

2. **For Game Implementation**:
   - Copy `playable_script.rpy` to the game directory and rename it to `script.rpy`
   - Adjust any asset paths or character definitions as needed
   - Test in the Ren'Py engine and refine

3. **For Rapid Testing**:
   - Use `renpy_game_player.py` to test dialogue flow and game logic
   - Debug variable states and conditions without loading full Ren'Py
   - Save and load game states for testing specific scenes

4. **For Future Episodes**:
   - Use the same structure as in `script.md` 
   - Follow the three-approach pattern for player choices
   - Maintain continuity with the player's final choice in Episode 1

## Game Structure

The game follows a 6-scene structure:

1. **Character Creation**: Player chooses a background that determines their stats
2. **Introduction**: Setting up the problem and introducing characters
3. **At the Link Loader**: Examining the problem and choosing an approach
4. **The Repair**: Different paths based on player's approach
5. **Confrontation**: Dealing with the antagonists
6. **Resolution**: Wrapping up the current mission and setting up future adventures

## Stats System

The game features three main stats that affect dialogue options and problem-solving approaches:
- **Cosmonaut (COS)**: Space/high-tech skills
- **Cowboy (COW)**: Desert/low-tech skills
- **Coder (COD)**: Robot communication/terminal skills

## Documentation

- **SCRIPT_PLAYER.md**: Detailed documentation for the script players
- **SCRIPT_TOOLS.md**: Documentation for script manipulation tools
- **DIALOGUE_TOOLS.md**: Documentation for the dialogue system